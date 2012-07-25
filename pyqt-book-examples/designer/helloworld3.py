# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui_helloworld import Ui_MainWindow

def main(argv):
    app = QtGui.QApplication(argv)

    mainwindow = MyMainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.setupUi(self)
        self.createConnects()

    def createConnects(self):
        self.pushButton.clicked.connect(self.textAktualisieren)
        self.lineEdit.textChanged.connect(self.label.setText)
    
    @QtCore.pyqtSlot()
    def textAktualisieren(self):
        self.label.setText(self.lineEdit.text())

if __name__ == "__main__":
    main(sys.argv)

