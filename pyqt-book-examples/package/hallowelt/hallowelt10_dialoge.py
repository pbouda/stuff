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
        #QtGui.QMessageBox.about(self,
        #    self.tr(u"Über \"Hallo Welt\""),
        #    self.tr(u"Hallo Welt - Begrüsst die Welt auf eine\
        #        einzigartige Art und Weise. Um mehr über\
        #        Qt-Programmierung zu erfahren besuchen Sie\
        #        unsere Website:\
        #        <a href=\"http://www.dasskript.com\">dasskript.com</a>")
        #    )
        
        #status = QtGui.QMessageBox.question(
        #    self, self.tr(u"Über \"Hallo Welt\""),
        #    self.tr(u"Möchten Sie jetzt für diese Anwendung spenden?"),
        #    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No
        #    )
        #if (status == QtGui.QMessageBox.Yes):
        #    QtGui.QDesktopServices.openUrl(
        #        QtCore.QUrl("https://www.paypal.com/cgi-bin/webscr?\
        #                    cmd=_s-xclick&hosted_button_id=VXN9T26P6HVLG")
        #    )
        
        #QtGui.QMessageBox.warning(self,
        #    self.tr(u"Über \"Hallo Welt\""),
        #    self.tr(u"Diese Anwendung ist sehr trivial.\n\
#Benutzung auf eigene Gefahr.")
        #)

        status = QtGui.QMessageBox.critical(
            self, self.tr(u"Über \"Hallo Welt\""),
            self.tr(u"Diese Anwendung macht gar nicht.\n\
Möchten Sie die Anwendung jetzt Schließen?"),
            QtGui.QMessageBox.Close, QtGui.QMessageBox.Ignore)
        if (status == QtGui.QMessageBox.Close):
            self.close();
    
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

