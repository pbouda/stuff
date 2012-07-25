# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui_helloworld import Ui_MainWindow
from ui_hellodialog import Ui_Dialog

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
        dialog = QtGui.QDialog(self)
        ui_dialog = Ui_Dialog()
        ui_dialog.setupUi(dialog)
        ui_dialog.pushButton.clicked.connect(dialog.accept)
        dialog.exec_()

    def createConnects(self):
        self.ui.pushButton.clicked.connect(self.textAktualisieren)
        self.ui.lineEdit.textChanged.connect(self.ui.label.setText)
    
    @QtCore.pyqtSlot()
    def textAktualisieren(self):
        self.ui.label.setText(self.ui.lineEdit.text())

if __name__ == "__main__":
    main(sys.argv)

