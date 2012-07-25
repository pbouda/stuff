# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from ui_helloworld import Ui_MainWindow

def main(argv):
    app = QtGui.QApplication(argv)

    language = unicode(QtCore.QLocale.system().name())

    qtTranslator = QtCore.QTranslator()
    qtTranslator.load("qt_{0}".format(language), QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    myappTranslator = QtCore.QTranslator()
    myappTranslator.load(":/translations/helloworld_{0}".format(language))
    app.installTranslator(myappTranslator)

    mainwindow = MyMainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createConnects()
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(":/images/pyqt_logo.png"))
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)

    def createConnects(self):
        self.ui.pushButton.clicked.connect(self.textAktualisieren)
        self.ui.lineEdit.textChanged.connect(self.ui.label.setText)
    
    @QtCore.pyqtSlot()
    def textAktualisieren(self):
        self.ui.label.setText(self.ui.lineEdit.text())

if __name__ == "__main__":
    main(sys.argv)

