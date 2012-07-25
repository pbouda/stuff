# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.labelHalloWelt = QtGui.QLabel(self.tr(u"Hello Welt!"));
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr(u"Aktualisieren"));
        self.editText = QtGui.QLineEdit()
        self.setWindowTitle(self.tr(u"Hallo Welt"))

        #widgetZentral = QtGui.QWidget()

        layoutZentral = QtGui.QVBoxLayout()
        layoutZentral.addWidget(self.labelHalloWelt)
        layoutZentral.addWidget(self.editText)
        layoutZentral.addWidget(self.buttonTextAktualisieren)

        #widgetZentral.setLayout(layoutZentral)
        self.setLayout(layoutZentral)
        #self.setCentralWidget(widgetZentral)

if __name__ == "__main__":
    main(sys.argv)

