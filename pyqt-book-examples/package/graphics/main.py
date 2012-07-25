# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os
import re
from PyQt4 import QtCore, QtGui

def main(argv):
  app = QtGui.QApplication(argv)
  main = PhotoViewerWindow()
  main.show()
  sys.exit(app.exec_())

class PhotoViewer(QtGui.QDialog):
    def __init__(self, parent, filepath):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Foto Viewer")
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.graphicsview = QtGui.QGraphicsView(self)
        self.pixmap = QtGui.QPixmap(filepath)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.graphicsview)
        self.setLayout(layout)

    def resizeEvent(self, event):        
        self.scalePixmap()
        self.showPixmap()

    def scalePixmap(self):
        self.scaledPixmap = \
            self.pixmap.scaled(QtCore.QSize(self.graphicsview.width()-5,
                                            self.graphicsview.height()-5),
                               QtCore.Qt.KeepAspectRatio)

    def showPixmap(self):
        self.graphicsscene = QtGui.QGraphicsScene(self)
        pixmapitem = self.graphicsscene.addPixmap(self.scaledPixmap)
        self.graphicsview.setScene(self.graphicsscene)
        

class PhotoBrowser(QtGui.QGraphicsScene):

    def __init__(self, parent, directory):
        QtGui.QGraphicsScene.__init__(self, parent)
        self.directory = directory
        self.fileList = []
        self.pixmaps = []
        self.initFileList()

    def initFileList(self):
        flist = os.listdir(self.directory)
        imageextension = re.compile("(?:[Jj][Pp][Ee]?[Gg]|[Pp][Nn][Gg])$")
        self.fileList = []
        for filename in flist:
            if imageextension.search(filename):
                self.fileList.append(filename)
        self.fileList.sort()

    def loadPhotos(self):
        progress = QtGui.QProgressDialog(
            self.tr("Loading photos..."),
            self.tr("Abort"),
            0,
            len(self.fileList),
            self.parent())
        progress.setWindowModality(QtCore.Qt.WindowModal)
        y = 0
        i = 0
        for filename in self.fileList:
            progress.setValue(i)
            filepath = os.path.join(self.directory, filename)
            pixmap = QtGui.QPixmap(filepath)
            pixmap = pixmap.scaled(QtCore.QSize(500,500),
                                   QtCore.Qt.KeepAspectRatio)
            pixmapitem = self.addPixmap(pixmap)
            textitem = self.addSimpleText(filename)
            textitem.setPos(QtCore.QPointF(0, pixmap.height()+5))
            itemGroup = self.createItemGroup([pixmapitem, textitem])
            itemGroup.setPos(QtCore.QPointF((300-pixmap.width())/2, y+10))
            itemGroup.setData(0, QtCore.QVariant(filename))
            itemGroup.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
            y = y + pixmap.height() + 50
            i = i + 1
            if (progress.wasCanceled()):
                self.clear()
                break
        progress.setValue(len(self.fileList))
        return len(self.fileList)

    def mouseDoubleClickEvent(self, event):
        filename = self.currentFilename()
        if filename:
            filepath = os.path.join(self.directory, filename)
            fotoviewer = PhotoViewer(self.parent(), filepath)
            fotoviewer.show()

    def currentFilename(self):
        if not self.selectedItems():
            return None
        else:
            return unicode(self.selectedItems()[0].data(0).toString())


class PhotoViewerWindow(QtGui.QMainWindow):
    
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)

        self.createComponents()
        self.createLayout()
        self.createConnects()

        self.currentDirectory = ""
        
        self.resize(600, 600)
        self.setWindowTitle(self.tr("Photo Viewer"))

    def createComponents(self):
        self.buttonSelectDir = QtGui.QPushButton(self.tr("Select directory"))
        self.editCurrentDir = QtGui.QLineEdit()
        self.graphicsviewPhotos = QtGui.QGraphicsView()
        self.photobrowser = QtGui.QGraphicsScene()
        self.graphicsviewPhotos.setScene(self.photobrowser)
        
    def createLayout(self):
        layoutCentral = QtGui.QVBoxLayout()

        layoutHoriz = QtGui.QHBoxLayout()
        layoutHoriz.addWidget(self.editCurrentDir)
        layoutHoriz.addWidget(self.buttonSelectDir)
        layoutCentral.addLayout(layoutHoriz)
        
        layoutCentral.addWidget(self.graphicsviewPhotos)
        
        widgetCentral = QtGui.QWidget()
        widgetCentral.setLayout(layoutCentral)
        self.setCentralWidget(widgetCentral)
        
    def createConnects(self):
        self.editCurrentDir.returnPressed.connect(self.loadPhotos)
        self.buttonSelectDir.clicked.connect(self.fileBrowser)
 
    @QtCore.pyqtSlot()
    def loadPhotos(self):
        self.currentDirectory = unicode(self.editCurrentDir.text())
        self.statusBar().showMessage(self.tr("Loading photos..."))
        self.photobrowser = PhotoBrowser(self, self.currentDirectory)
        count = self.photobrowser.loadPhotos()
        self.graphicsviewPhotos.setScene(self.photobrowser)
        self.statusBar().showMessage(
            unicode(self.tr("{0} photos")).format(count))
  
    @QtCore.pyqtSlot()
    def fileBrowser(self):
        dialog = QtGui.QFileDialog(self, self.tr("Select Directory"),
                                   QtGui.QDesktopServices.storageLocation(
                                    QtGui.QDesktopServices.PicturesLocation))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        if (dialog.exec_()):
            self.editCurrentDir.setText(unicode(dialog.selectedFiles()[0]))
            self.loadPhotos()

if __name__ == "__main__":
    main(sys.argv)
