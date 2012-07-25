# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtGui.QMainWindow):

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
        dialog = QtGui.QDialog(self)
        label = QtGui.QLabel(self.tr(u"Klicke den Button"), dialog)
        button = QtGui.QPushButton(
            self.tr(u"Schließe mich"), dialog)
        layoutDialog = QtGui.QHBoxLayout()
        layoutDialog.addWidget(label)
        layoutDialog.addWidget(button)
        #layoutDialog.addWidget(buttonAbbrechen)
        dialog.setLayout(layoutDialog)
        dialog.setWindowTitle(self.tr(u"Hallo Welt Dialog"))
        button.clicked.connect(dialog.accept)
        #buttonAbbrechen.clicked.connect(dialog.reject)
        result = dialog.exec_()
        #if result == QtGui.QDialog.Accepted:
        #    print u"OK, es wurde nicht abgebrochen"
        #dialog.show()
        
        #dialog = QtGui.QDialog(self)
        #eingabe = QtGui.QLineEdit(dialog)
        #buttonOk = QtGui.QPushButton(
        #    self.tr("OK"), dialog)
        #buttonAbbrechen = QtGui.QPushButton(
        #    self.tr("Abbrechen"), dialog)
        #layoutDialog = QtGui.QHBoxLayout()
        #layoutDialog.addWidget(eingabe)
        #layoutDialog.addWidget(buttonOk)
        #layoutDialog.addWidget(buttonAbbrechen)
        #dialog.setLayout(layoutDialog)
        #buttonOk.clicked.connect(dialog.accept)
        #buttonAbbrechen.clicked.connect(dialog.reject)
        #result = dialog.exec_()
        #if result == QtGui.QDialog.Accepted:
        #    eingabe = unicode(eingabe.text())
        #    print eingabe
        #else:
        #    print "Abgebrochen"

        #dialog = MeinDialog(self)
        #dialog.exec_()
        #print dialog.eingabe

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

class MeinDialog(QtGui.QDialog):
    
    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        self.createComponents()
        self.createLayout()
        self.createConnects()
        self.setWindowTitle(self.tr(u"Mein Dialog"))
        
    def createComponents(self):
        self.lineeditEingabe = QtGui.QLineEdit()
        self.button = QtGui.QPushButton(self.tr(u"Schließe mich"))
        
    def createLayout(self):
        layoutDialog = QtGui.QHBoxLayout()
        layoutDialog.addWidget(self.lineeditEingabe)
        layoutDialog.addWidget(self.button)
        self.setLayout(layoutDialog)
        
    def createConnects(self):
        self.button.clicked.connect(self.accept)

    @property
    def eingabe(self):
        eingabe = unicode(self.lineeditEingabe.text())
        return eingabe

if __name__ == "__main__":
    main(sys.argv)

