# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)

    QtGui.QApplication.setApplicationName("HalloWelt")

    qtTranslator = QtCore.QTranslator()
    qtTranslator.load("qt_" + unicode(QtCore.QLocale.system().name()), QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    myappTranslator = QtCore.QTranslator()
    myappTranslator.load("lokalisierung_" + unicode(QtCore.QLocale.system().name()))
    app.installTranslator(myappTranslator)

    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow):

    meinSignal = QtCore.pyqtSignal()

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.createMenu()
        self.createComponents()
        self.createLayout()
        self.createConnects()

        self.setWindowTitle(self.tr(u"Hallo Welt"))

    def createMenu(self):
        self.actionDateiOeffnen = QtGui.QAction(self.tr(u"Datei öffnen..."), self)
        self.actionDateiSpeichern = QtGui.QAction(self.tr(u"Speichern"), self)
        self.actionBeenden = QtGui.QAction(self.tr(u"Beenden"), self)
        self.actionBeenden.setMenuRole(QtGui.QAction.QuitRole)

        menuDatei = self.menuBar().addMenu(self.tr(u"Datei"))
        menuDatei.addAction(self.actionDateiOeffnen)
        menuDatei.addAction(self.actionDateiSpeichern)

        actiongroupAnsichten = QtGui.QActionGroup(self)
        #self.actionLinksAusrichten = QtGui.QAction(self.tr(u"Links Ausrichten"), self)
        self.actionLinksAusrichten = QtGui.QAction(self.tr(u"Links Ausrichten"), actiongroupAnsichten)
        self.actionLinksAusrichten.setCheckable(True)
        self.actionLinksAusrichten.setChecked(True)
        #self.actionRechtsAusrichten = QtGui.QAction(self.tr(u"Rechts Ausrichten"), self)
        self.actionRechtsAusrichten = QtGui.QAction(self.tr(u"Rechts Ausrichten"), actiongroupAnsichten)
        self.actionRechtsAusrichten.setCheckable(True)
        actiongroupAnsichten.setExclusive(False)
        
        menuAnsicht = menuDatei.addMenu(self.tr(u"Ansicht"))
        menuAnsicht.addAction(self.actionLinksAusrichten)
        menuAnsicht.addAction(self.actionRechtsAusrichten)

        menuDatei.addSeparator()
        menuDatei.addAction(self.actionBeenden)
        
        self.actionUeber = QtGui.QAction(self.tr(u"Über Hallo Welt..."), self)
        menuUeber = self.menuBar().addMenu(self.tr(u"Hilfe"))
        menuUeber.addAction(self.actionUeber)

    def createComponents(self):
        self.labelHalloWelt = QtGui.QLabel(self.tr(u"Hallo Welt!"));
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr(u"Aktualisieren"));
        self.editText = QtGui.QLineEdit()

    def createConnects(self):
        self.buttonTextAktualisieren.clicked.connect(self.textAktualisieren)
        self.editText.textChanged.connect(self.labelHalloWelt.setText)
        self.actionUeber.triggered.connect(self.zeigeUeberDialog)

    @QtCore.pyqtSlot()
    def zeigeUeberDialog(self):
        print u"Hier kommt der Dialog"
    
    @QtCore.pyqtSlot()
    def textAktualisieren(self):
        self.labelHalloWelt.setText(self.editText.text())

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

