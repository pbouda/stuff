# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.ui_helloworld import Ui_MainWindow

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
