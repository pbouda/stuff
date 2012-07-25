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

        self.setWindowTitle(self.tr(u"Hallo Welt"))

        #settings = QtCore.QSettings("dasskript.com", "HalloWelt")
        #stringEingabe = unicode(settings.value(
        #    "stringEingabe", "Hallo Welt!").toString())
        #self.editText.setText(stringEingabe)

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
        pass

    def createLayout(self):
        layoutZentral = QtGui.QVBoxLayout()
        layoutZentral.addWidget(self.labelHalloWelt)
        layoutZentral.addWidget(self.editText)
        layoutZentral.addWidget(self.buttonTextAktualisieren)
        
        widgetZentral = QtGui.QWidget()
        widgetZentral.setLayout(layoutZentral)
        self.setCentralWidget(widgetZentral)

    def resizeEvent(self, event):
        print u"Neue Breite: %i" % event.size().width()
        print u"Neue Höhe: %i" % event.size().height()
        QtGui.QMainWindow.resizeEvent(self, event)

    def closeEvent(self, event):
        settings = QtCore.QSettings("dasskript.com", "HalloWelt")
        stringEingabe = self.editText.text()
        settings.setValue("stringEingabe", stringEingabe);
        event.accept()
        
    def changeEvent(self, event):
        QtGui.QMainWindow.changeEvent(self, event)
        if event.type() == QtCore.QEvent.LanguageChange:
            print "Neue Sprache..."
            self.retranslateUi()
            
    def retranslateUi():
        self.labelHalloWelt.setText(self.tr(u"Hallo Welt!"))
        self.buttonTextAktualisieren.setText(self.tr(u"Aktualisieren"))

if __name__ == "__main__":
    main(sys.argv)

