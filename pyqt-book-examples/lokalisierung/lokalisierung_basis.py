# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.createComponents()
        self.createLayout()

        self.setWindowTitle(self.tr("Hello World"))
        
    def createComponents(self):
        self.labelHalloWelt = QtGui.QLabel(self.tr("Hello World!"))
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr("Update"))
        self.editText = QtGui.QLineEdit()

    def createLayout(self):
        layoutZentral = QtGui.QVBoxLayout()
        layoutZentral.addWidget(self.labelHalloWelt)
        layoutZentral.addWidget(self.editText)
        layoutZentral.addWidget(self.buttonTextAktualisieren)
        
        widgetZentral = QtGui.QWidget()
        widgetZentral.setLayout(layoutZentral)
        self.setCentralWidget(widgetZentral)


if __name__ == "__main__":
    main(sys.argv)


