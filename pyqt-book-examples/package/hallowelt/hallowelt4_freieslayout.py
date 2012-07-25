# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.createMenu()
        self.createComponents()
        #self.createLayout()
        self.createConnects()

        self.setWindowTitle(self.tr("Hello World"))
        self.resize(500, 250)

    def createMenu(self):
    	pass

    def createComponents(self):
        self.labelHalloWelt = QtGui.QLabel(self.tr("Hello World!"), self);
        self.labelHalloWelt.setGeometry(20, 20, 100, 50)
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr(u"Update"), self)
        self.buttonTextAktualisieren.setGeometry(20, 100, 150, 50)
        self.editText = QtGui.QLineEdit(self)
        self.editText.setGeometry(220, 100, 200, 50)

    def createConnects(self):
        pass

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

