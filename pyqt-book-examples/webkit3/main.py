#!/usr/bin/env python

import os, sys, optparse
from PySide import QtCore, QtGui, QtDeclarative

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option("-f", "--fullscreen", dest="fullscreen", help="Start application in fullscreen mode", action="store_true", default=False)
    
    (options, args) = parser.parse_args()
    
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setSource(QtCore.QUrl("main.qml"))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    if options.fullscreen:
        from PySide import QtOpenGL
        glw = QtOpenGL.QGLWidget()
        view.setViewport(glw)
        view.showFullScreen()
    else:
        view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)