# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui_helloworld import Ui_MainWindow

def main(argv):
    app = QtGui.QApplication(argv)

    mainwindow = MyMainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createConnects()

    def createConnects(self):
        self.ui.pushButton.clicked.connect(self.textAktualisieren)
        self.ui.lineEdit.textChanged.connect(self.ui.label.setText)
    
    @QtCore.pyqtSlot()
    def textAktualisieren(self):
        self.ui.label.setText(self.ui.lineEdit.text())

if __name__ == "__main__":
    main(sys.argv)

