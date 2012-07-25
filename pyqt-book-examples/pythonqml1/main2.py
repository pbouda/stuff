#!/usr/bin/env python

import sys, os, traceback
from PyQt4 import QtCore, QtGui, QtDeclarative

def main(argv):
    app = QtGui.QApplication(argv)
    main = QtGui.QMainWindow()
    view = QtDeclarative.QDeclarativeView(main)

    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeViewToRootObject)
    view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    
    view.setSource(QtCore.QUrl("main2.qml"))
    
    main.setCentralWidget(view)
    main.resize(360, 480)
    main.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
