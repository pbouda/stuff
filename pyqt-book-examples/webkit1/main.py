#!/usr/bin/env python

import sys, os
import re
from PyQt4 import QtCore, QtGui
from ui_main import Ui_MainWindow

def main(argv):
    app = QtGui.QApplication(argv)
    MainWindow = BrowserWindow()
    MainWindow.show()
    sys.exit(app.exec_())

class BrowserWindow(QtGui.QWidget):
    """Das Hauptfenster des Browsers."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createConnects()

    def createConnects(self):
        self.ui.editAddress.returnPressed.connect(self.loadPage)
        self.ui.webView.urlChanged.connect(self.updateUrl)
        self.ui.buttonBack.clicked.connect(self.ui.webView.back)
        self.ui.buttonForward.clicked.connect(self.ui.webView.forward)
        self.ui.buttonReload.clicked.connect(self.ui.webView.reload)

    @QtCore.pyqtSlot(QtCore.QUrl)
    def updateUrl(self, url):
        self.ui.editAddress.setText(url.toString())

    @QtCore.pyqtSlot()
    def loadPage(self):
        stringUrl = unicode(self.ui.editAddress.text())
        if not re.search(r"^http", stringUrl):
            stringUrl = "http://" +stringUrl
        url = QtCore.QUrl(stringUrl)
        self.ui.webView.load(url)
        self.ui.editAddress.clearFocus()
        
if __name__ == "__main__":
    main(sys.argv)
