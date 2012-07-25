
# -*- coding: utf-8 -*-

import sys, numpy
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class RenderThread(QtCore.QThread):
    
    __pyqtSignals__ =  ( "imageRendered(QImage)" )
    
    def __init__(self, *args):
        QtCore.QThread.__init__(self, *args)
        
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        
        self.restart = False
        self.abort = False
        self.ColormapSize = 512
        self.colormap = [ self.rgbFromWaveLength(380.0 + (i * 400.0 / self.ColormapSize)) for i in range(self.ColormapSize) ]
    
    def __del__(self):
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()
        
    def render(self, centerX, centerY, scaleFactor, resultSize):
        with QtCore.QMutexLocker(self.mutex) as locker:
            self.centerX = centerX
            self.centerY = centerY
            self.scaleFactor = scaleFactor
            self.resultSize = resultSize
            
            if not self.isRunning():
                self.start(self.LowPriority)
            else:
                self.restart = True
                self.condition.wakeOne()
    
    def run(self):
        while True:
            self.mutex.lock()
            resultSize = self.resultSize
            scaleFactor = self.scaleFactor
            centerX = self.centerX
            centerY = self.centerY
            self.mutex.unlock()
            
            halfWidth = resultSize.width() / 2
            halfHeight = resultSize.height() / 2
            image = QtGui.QImage(resultSize, QtGui.QImage.Format_RGB32)
            numPasses = 8
            curPass = 0
            
            while(curPass < numPasses):
                maxIterations = (1 << (2*curPass + 6)) + 32
                limit = 4
                allBlack = True
                
                for y in range(-halfHeight, halfHeight):
                    if self.restart:
                        break
                    if self.abort:
                        return
                    
                    scanLine = image.scanLine(y + halfHeight)
                    scanLine.setsize(32*resultSize.width())
                    scanLinePointer = numpy.frombuffer(scanLine, numpy.uint32)
                    i = 0
                    ay = centerY + (y * scaleFactor)
                    
                    for x in range(-halfWidth, halfWidth):
                        ax = centerX + (x * scaleFactor)
                        a1 = ax
                        b1 = ay
                        
                        numIterations = 0
                        
                        while (numIterations < (maxIterations + 1)):
                            numIterations = numIterations + 1
                            a2 = (a1 * a1) - (b1 * b1) + ax
                            b2 = (2 * a1 * b1) + ay
                            if (a2 * a2) + (b2 * b2) > limit:
                                break
                            
                            numIterations = numIterations + 1
                            a1 = (a2 * a2) - (b2 * b2) + ax
                            b1 = (2 * a2 * b2) + ay
                            if (a1 * a1) + (b1 * b1) > limit:
                                break
                            
                        if (numIterations < maxIterations):
                            scanLinePointer[i] = self.colormap[numIterations % self.ColormapSize]
                            allBlack = False
                        else:
                            scanLinePointer[i] = QtGui.qRgb(0, 0, 0)
                        i = i + 1
                        #print i
                
                if allBlack and (curPass == 0):
                    curPass = 4
                else:
                    if not self.restart:
                        self.emit(QtCore.SIGNAL("imageRendered(QImage, double)"), image, scaleFactor)
                    curPass = curPass + 1
                    
            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()
                

    def rgbFromWaveLength(self, wave):
        r = 0.0
        g = 0.0
        b = 0.0
        
        if wave >= 380.0 and wave <= 440.0:
            r = -1.0 * (wave - 440.0) / (440.0 - 380.0)
            b = 1.0
        elif wave >= 440.0 and wave <= 490.0:
            g = (wave - 440.0) / (490.0 - 440.0)
            b = 1.0
        elif wave >= 490.0 and wave <=510.0:
            g = 1.0
            b = -1.0 * (wave - 510.0) / (510.0 - 490.0)
        elif wave >= 510.0 and wave <= 580.0:
            r = (wave - 510.0) / (580.0 - 510.0)
            g = 1.0
        elif wave >= 580.0 and wave <= 645.0:
            r = 1.0
            g = -1.0 * (wave - 645.0) / (645.0 - 580.0)
        elif wave >= 645.0 and wave <= 780.0:
            r = 1.0
        
        s = 1.0
        if wave > 700.0:
            s = 0.3 + 0.7 * (780.0 - wave) / (780.0 - 700.0)
        elif wave < 420.0:
            s = 0.3 + 0.7 * (wave - 380.0) / (420.0 - 380.0)
            
        r = pow(r*s, 0.8)
        g = pow(g*s, 0.8)
        b = pow(b*s, 0.8)
        return QtGui.qRgb(int(r*255), int(g*255), int(b*255))

    
class MainWindow(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.centerX = -0.637011
        self.centerY = -0.0395159
        self.pixmapScale = 0.00403897
        self.curScale = 0.00403897
        
        self.ZoomInFactor = 0.8
        self.ZoomOutFactor = 1.0 / self.ZoomInFactor
        self.ScrollStep = 20
        
        self.pixmap = None
        self.pixmapOffset = QtCore.QPoint()
        self.setWindowTitle("Apfelmann")
        self.thread = RenderThread(self)
        self.connect(self.thread, QtCore.SIGNAL("imageRendered(QImage, double)"), self.updatePixmap)
        self.resize(550, 400)
        
    def __del__(self):
        self.thread.__del__()

    def paintEvent(self, paintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)
        
        if self.pixmap is None:
           painter.setPen(QtCore.Qt.white)
           painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self.tr("Rendering image, please wait..."))
           return
        
        if self.curScale == self.pixmapScale:
            painter.drawPixmap(self.pixmapOffset, self.pixmap)
        else:
            scaleFactor = self.pixmapScale / self.curScale
            newWidth = int(self.pixmap.width() * scaleFactor)
            newHeight = int(self.pixmap.height() * scaleFactor)
            newX = self.pixmapOffset.x() + (self.pixmap.width() - newWidth) / 2
            newY = self.pixmapOffset.y() + (self.pixmap.height() - newHeight) / 2
            
            painter.save()
            painter.translate(newX, newY)
            painter.scale(scaleFactor, scaleFactor)
            exposed = painter.matrix().inverted()[0].mapRect(self.rect()).adjusted(-1, -1, 1, 1)
            painter.drawPixmap(exposed, self.pixmap, exposed)
            painter.restore()
            
        text = self.tr("Use mouse wheel or the '+' and '-' keys to zoom. Press and hold left mouse button to scroll.")
        metrics = painter.fontMetrics()
        textWidth = metrics.width(text)
        
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 127))
        painter.drawRect((self.width() - textWidth) / 2 - 5, 0, textWidth + 10, metrics.lineSpacing() + 5)
        painter.setPen(QtCore.Qt.white)
        painter.drawText((self.width() - textWidth) / 2, metrics.leading() + metrics.ascent(), text)
        
    def resizeEvent(self, resizeEvent):
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())
        
    def keyPressEvent(self, keypressEvent):
        key = keypressEvent.key()
        if key == QtCore.Qt.Key_Plus:
            self.zoom(self.ZoomInFactor)
        elif key == QtCore.Qt.Key_Minus:
            self.zoom(self.ZoomOutFactor)
        elif key == QtCore.Qt.Key_Left:
            self.scroll(-self.ScrollStep, 0)
        elif key == QtCore.Qt.Key_Right:
            self.scroll(self.ScrollStep, 0)
        elif key == QtCore.Qt.Key_Down:
            self.scroll(0, -self.ScrollStep)
        elif key == QtCore.Qt.Key_Up:
            self.scroll(0, self.ScrollStep)
        QtGui.QWidget.keyPressEvent(self, keypressEvent)
        
    def updatePixmap(self, image, scaleFactor):
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.pixmapOffset = QtCore.QPoint()
        self.pixmapScale = self.curScale
        self.update()
        
    def zoom(self, zoomFactor):
        self.curScale = self.curScale * zoomFactor
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())
        
    def scroll(self, deltaX, deltaY):
        self.centerX = self.centerX + deltaX * self.curScale
        self.centerY = self.centerY + deltaY * self.curScale
        self.pixmapOffset = self.pixmapOffset - QtCore.QPoint(deltaX, deltaY)
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())

        
if __name__ == "__main__":
    main(sys.argv)