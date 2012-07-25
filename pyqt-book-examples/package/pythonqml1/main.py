#!/usr/bin/env python

import sys, os, traceback
from PySide import QtCore, QtGui, QtDeclarative

def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setSource(QtCore.QUrl("main.qml"))
    #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeViewToRootObject)
    view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
