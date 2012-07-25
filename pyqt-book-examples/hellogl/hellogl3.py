# -*- coding: utf-8 -*-

import sys, random
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *

livingSpace = []
livingSpaceWidth = 100
livingSpaceHeight = 60
creatureSize = 10


def main(argv):

    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtOpenGL.QGLWidget):

    def __init__(self, *args):
        QtOpenGL.QGLWidget.__init__(self, *args)

        self.initLivingSpace()
        self.resize(livingSpaceWidth * creatureSize, livingSpaceHeight * creatureSize)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateWorld)
        self.timer.start(40)

    def updateWorld(self):
        self.calculateNextGeneration()
        self.updateGL()
        
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))
        
        #glShadeModel(GL_SMOOTH)
        #glClearDepth(1.0)
        #glMatrixMode(GL_PROJECTION)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, 3.0)
        glBegin(GL_QUADS)
        for column in range(livingSpaceWidth):
            for row in range(livingSpaceHeight):
                healthStatus = float(livingSpace[column][row]) / 1000.0
                # die Farbe fuer die belebten Felder wird
                # nun in Abhaengigkeit vom Wert des Feldes bestimmt
                glColor4f(healthStatus, 0.0, 0.0, 1.0)
                x = column * 10.0
                y = row * 10.0
                glVertex3f(x, y, 0.0)
                glVertex3f(9.0 + x, y, 0.0)
                glVertex3f(9.0 + x, 9.0 + y, 0.0)
                glVertex3f(x, 9.0 + y, 0.0)
        glEnd()
        
    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10.0, livingSpaceWidth * 10.0 + 10.0, livingSpaceHeight * 10.0 + 10.0, -10.0, -6.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glViewport(0, 0, w, h);
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()

    def initLivingSpace(self):
        for x in range(livingSpaceWidth):
            livingSpace.append([])
            for y in range(livingSpaceHeight):
                if random.randint(0, 1) == 1:
                    livingSpace[x].append(1000)
                else:
                    livingSpace[x].append(0)

    def isAlive(self, x, y):
        return livingSpace[x][y] == 1000
    
    def getNeighborCount(self, x, y):
        count = 0
        
        xpn = (x + 1) % livingSpaceWidth
        ypn = (y + 1) % livingSpaceHeight
            
        count += self.isAlive(x  , ypn)
        count += self.isAlive(xpn, ypn)
        count += self.isAlive(xpn, y)
        count += self.isAlive(xpn, y - 1)
        count += self.isAlive(x  , y - 1)
        count += self.isAlive(x - 1, y - 1)
        count += self.isAlive(x - 1, y)
        count += self.isAlive(x - 1, ypn)
        return count
    
    def calculateNextGeneration(self):
        neighborCount = []
        for column in range(livingSpaceWidth):
            neighborCount.append([])
            for row in range(livingSpaceHeight):
                neighborCount[column].append(self.getNeighborCount(column, row))
                
        for column in range(livingSpaceWidth):
            for row in range(livingSpaceHeight):
                if 2 <= neighborCount[column][row] <= 3:
                    if neighborCount[column][row] == 3:
                        # Geburt eines Lebewesens
                        livingSpace[column][row] = 1000
                else:
                    # langsamer Tod eines Lebewesens
                    livingSpace[column][row] = livingSpace[column][row]/1.1
                
                if livingSpace[column][row] < 200:
                    livingSpace[column][row] = 0

if __name__ == "__main__":
    main(sys.argv)