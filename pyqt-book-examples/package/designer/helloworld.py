# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui_helloworld import Ui_MainWindow

def main(argv):
    app = QtGui.QApplication(argv)

    mainwindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)

