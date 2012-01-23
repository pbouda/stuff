#!/usr/bin/env python

import sys, os
from PyQt4 import QtCore, QtGui, QtDeclarative, QtOpenGL

def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    
    app.setOverrideCursor( QtGui.QCursor( QtCore.Qt.BlankCursor ) )
    view.setSource(QtCore.QUrl("qml/main2.qml"))
    glw = QtOpenGL.QGLWidget()
    view.setViewport(glw)
    view.showFullScreen()
    
    #view.resize(800, 600)
    view.show()

    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
