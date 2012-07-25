# -*- coding: utf-8 -*-

import sys, numpy
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtOpenGL.QGLWidget):

    def __init__(self, *args):
        QtOpenGL.QGLWidget.__init__(self, *args)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)
        
    def sizeHint(self):
        return QtCore.QSize(400, 400)
        
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))
        
        glShadeModel(GL_SMOOTH)
        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)

    def paintGL(self):
        glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor(0.1, 0.5, 0.8)
        glBegin(OpenGL.GL.GL_TRIANGLES)
        glVertex3f( 0.0, 0.5, 0.0) 
        glVertex3f(-0.5,-0.5, 0.0)
        glVertex3f( 0.5,-0.5, 0.0)
        glEnd()
        
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h);
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

if __name__ == "__main__":
    main(sys.argv)