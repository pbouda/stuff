# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Oct 12 10:11:20 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 510)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonBack = QtGui.QPushButton(MainWindow)
        self.buttonBack.setObjectName(_fromUtf8("buttonBack"))
        self.horizontalLayout.addWidget(self.buttonBack)
        self.buttonForward = QtGui.QPushButton(MainWindow)
        self.buttonForward.setObjectName(_fromUtf8("buttonForward"))
        self.horizontalLayout.addWidget(self.buttonForward)
        self.buttonReload = QtGui.QPushButton(MainWindow)
        self.buttonReload.setObjectName(_fromUtf8("buttonReload"))
        self.horizontalLayout.addWidget(self.buttonReload)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.editAddress = QtGui.QLineEdit(MainWindow)
        self.editAddress.setText(_fromUtf8(""))
        self.editAddress.setObjectName(_fromUtf8("editAddress"))
        self.verticalLayout_2.addWidget(self.editAddress)
        self.webView = QtWebKit.QWebView(MainWindow)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout_2.addWidget(self.webView)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Python Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBack.setText(QtGui.QApplication.translate("MainWindow", "Zurück", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonForward.setText(QtGui.QApplication.translate("MainWindow", "Vorwärts", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonReload.setText(QtGui.QApplication.translate("MainWindow", "Neu Laden", None, QtGui.QApplication.UnicodeUTF8))
        self.editAddress.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Hier die URL eingeben", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
