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
        self.createLayout()
        self.createConnects()

        self.setWindowTitle(self.tr("Hello World"))

    def createMenu(self):
        self.actionDateiOeffnen = QtGui.QAction(self.tr("Open File..."), self)
        self.actionDateiSpeichern = QtGui.QAction(self.tr("Speichern"), self)
        self.actionBeenden = QtGui.QAction(self.tr("Beenden"), self)
        self.actionBeenden.setMenuRole(QtGui.QAction.QuitRole)

        menuDatei = self.menuBar().addMenu(self.tr("File"))
        menuDatei.addAction(self.actionDateiOeffnen)
        menuDatei.addAction(self.actionDateiSpeichern)
        menuDatei.addSeparator()
        menuDatei.addAction(self.actionBeenden)
        
        self.actionUeber = QtGui.QAction(self.tr("About Hello World..."), self)
        menuUeber = self.menuBar().addMenu(self.tr("Help"))
        menuUeber.addAction(self.actionUeber)

    def createComponents(self):
        self.labelHalloWelt = QtGui.QLabel(self.tr("Hello World!"));
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr("Update"));
        self.editText = QtGui.QLineEdit()

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

