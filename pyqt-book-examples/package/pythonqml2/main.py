#!/usr/bin/env python

import sys, os, traceback
from PyQt4 import QtCore, QtGui, QtDeclarative

def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()

    colors = [ "red", "green", "blue" ]

    context = view.rootContext()
    context.setContextProperty("colorModel", colors)

    view.setSource(QtCore.QUrl("main.qml"))
    view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
