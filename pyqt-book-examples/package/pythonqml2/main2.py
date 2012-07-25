#!/usr/bin/env python

import sys, os, traceback
from PySide import QtCore, QtGui, QtDeclarative

def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    
    colors = [
        { "color": "red", "text": "Zeile 1" },
        { "color": "green", "text": "Zeile 2" },
        { "color": "blue", "text": "Zeile 3" }
    ]
    
    context = view.rootContext()
    context.setContextProperty("colorModel", colors)

    view.setSource(QtCore.QUrl("main2.qml"))
    view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
