# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    #mainwindow = QtGui.QMainWindow()
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.createMenu()
        self.createComponents()
        self.createLayout()
        self.selfAssignLayout()
        self.createConnects()

        self.setWindowTitle(self.tr(u"Hallo Welt"))

        settings = QtCore.QSettings("mobileqt.de", "HalloWelt")
        stringEingabe = unicode(settings.value("stringEingabe", "").toString())
        self.editText.setText(stringEingabe)


    def createMenu(self):
        #menuBar = QtGui.QMenuBar(self)
        #menuBar.addAction(self.aktionUeber)

        self.aktionDateiOeffnen = QtGui.QAction(self.tr(u"Datei Öffnen..."), self)
        self.aktionBeenden = QtGui.QAction(self.tr(u"Beenden"), self)
        self.aktionBeenden.setMenuRole(QtGui.QAction.QuitRole)
        self.aktionUeber = QtGui.QAction(self.tr(u"Über Hallo Welt"), self)

        menueDatei = self.menuBar().addMenu(self.tr(u"Datei"))
        menueDatei.addAction(self.aktionDateiOeffnen)
        menueDatei.addSeparator()
        menueDatei.addAction(self.aktionBeenden)

        menueUeber = self.menuBar().addMenu(self.tr(u"Über"))
        menueUeber.addAction(self.aktionUeber)

    def createComponents(self):
        self.labelHalloWelt = QtGui.QLabel(self.tr(u"Hallo Welt!"));
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr(u"Aktualisieren"));
        self.editText = QtGui.QLineEdit()
        #editText.installEventFilter(self)

    def createConnects(self):
        self.connect(self.buttonTextAktualisieren, QtCore.SIGNAL("clicked()"), self.textAktualisieren)
        self.connect(self.editText, QtCore.SIGNAL("textChanged(QString)"), self.labelHalloWelt.setText)
        self.connect(self.aktionUeber, QtCore.SIGNAL("triggered()"), self.zeigeUeberDialog)

    def zeigeUeberDialog(self):
        #status = QtGui.QMessageBox.critical(self, self.tr("Über \"Hallo Welt\""),
        #    tr("Diese Anwendung macht gar nicht. Möchten Sie die Anwendung jetzt Schließen?"),
        #    QtGui.QMessageBox.Ignore, QtGui.QMessageBox.Close);
        #if (status == QtGui.QMessageBox.Close):
        #    self.close();

        #status = QtGui.QMessageBox.question(self, tr("Über \"Hallo Welt\""),
        #    tr("Möchten Sie jetzt für diese Anwendung spenden?"),
        #    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        #if (status == QtGui.QMessageBox.Yes):
        #    QtGui.QDesktopServices.openUrl(
        #        QUrl("https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=VXN9T26P6HVLG"));

        ordnerpfad = QtGui.QFileDialog.getExistingDirectory(self, self.tr(u"Datei speichern"),
            QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation))
        print ordnerpfad;

        #ergebnis, ok = QtGui.QInputDialog.getDouble(
        #        self,
        #        self.tr("Schwierige Addition"),
        #        self.tr("Wieviel ist 5,6 plus 7,9?"),
        #        0, 0, 100, 2)
        #if ok:
        #    printergebnis;

        #werte = QtCore.QStringList()
        #werte.append(self.tr("Ist doch egal"))
        #werte.append(self.tr("Dreizehnkommafünf"))
        #werte.append(self.tr("Zwei"))
        #werte.append(self.tr("Der Mount Everest"))
        #ergebnis, ok = QtGui.QInputDialog.getItem(
        #        self,
        #        self.tr("Schwierige Addition"),
        #        self.tr("Wieviel ist 5,6 plus 7,9?"),
        #        werte, 0, False);
        #if ok:
        #    print ergebnis

        #eingabe, ok = QtGui.QInputDialog.getText(
        #    self,
        #    self.tr("Schwierige Frage"),
        #    self.tr("Was ist der höchste Berg der Welt?"),
        #    QtGui.QLineEdit.Password, "");
        #if ok:
        #    print eingabe;

        #dialog = QtGui.QDialog(self)
        #label = QtGui.QLabel(self.tr("Klicke den Button"), dialog)
        #button = QtGui.QPushButton(self.tr("Schließe mich"), dialog)
        #layoutDialog = QtGui.QHBoxLayout()
        #layoutDialog.addWidget(label)
        #layoutDialog.addWidget(button)
        #dialog.setLayout(layoutDialog)
        #self.connect(button, QtCore.SIGNAL(clicked()), dialog.accept())
        #dialog.exec_()

        #dialog = QtGui.QDialog(self)
        #eingabe = QtGui.QLineEdit(dialog)
        #buttonOk = QtGui.QPushButton(self.tr("OK"), dialog)
        #buttonAbbrechen = QtGui.QPushButton(self.tr("Abbrechen"), dialog)
        #layoutDialog = QtGui.QHBoxLayout()
        #layoutDialog.addWidget(eingabe)
        #layoutDialog.addWidget(buttonOk)
        #layoutDialog.addWidget(buttonAbbrechen)
        #dialog.setLayout(layoutDialog)
        #self.connect(buttonOk, SIGNAL(clicked()), dialog.accept())
        #sellf.connect(buttonAbbrechen, SIGNAL(clicked()), dialog.reject())
        #result = dialog.exec_();
        #if result == QtGui.QDialog.Accepted:
        #    print eingabe.text()
        #else:
        #    print "Abgebrochen"

        #MeinDialog dialog(self)
        #dialog.exec_()
        #print dialog.eingabe()

    def createLayout(self):
        self.layoutZentral = QtGui.QVBoxLayout()
        self.layoutZentral.addWidget(self.labelHalloWelt, 0, QtCore.Qt.AlignCenter)

        layoutHorizontal = QtGui.QHBoxLayout()
        layoutHorizontal.addWidget(self.editText)
        layoutHorizontal.addWidget(self.buttonTextAktualisieren)
    
        self.layoutZentral.addLayout(layoutHorizontal)

    def selfAssignLayout(self):
        widgetZentral = QtGui.QWidget()
        widgetZentral.setLayout(self.layoutZentral)
        self.setCentralWidget(widgetZentral)

    def textAktualisieren(self):
        self.labelHalloWelt.setText(self.editText.text())

    #def changeEvent(self, event):
    #    QtGui.QMainWindow.changeEvent(event)
    #    if event.type() == QtCore.QEvent.LanguageChange:
    #        self.retranslateUi()

    #def resizeEvent(self, event):
    #    print "Neue Breite: " + event.size().width()
    #    qDebug() << "Neue Höhe: " + event.size().height()
    #    QtGui.QMainWindow.resizeEvent(event)

    #def closeEvent(self, event):
    #    settings = QtCore.QSettings("mobileqt.de", "HalloWelt")
    #    stringEingabe = unicode(self.editText.text())
    #    settings.setValue("stringEingabe", stringEingabe)
    #    print "String: " + stringEingabe;
    #    event.accept()

    #def event(self, event):
    #    if event.type() == QtCore.QEvent.Resize:
    #        print "Resize"
    #        return True
    #    elif event.type() == QtCore.QEvent.Close:
    #        print "Close"
    #        return True
    #    elif event.type() == QtCore.QEvent.LanguageChange:
    #        print "LanguageChange"
    #        return True
    #    return QtGui.QMainWindow.event(event)

    #def eventFilter(self, obj, event):
    #    if event.type() == QtCore.QEvent.KeyPress:
    #        #QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
    #        if (event.key() == QtCore.Qt.Key_Exclam) or (event.key() == QtCore.Qt.Key_Question):
    #            print "Zeichen abgefangen."
    #            return True
    #    return QtCore.QObject.eventFilter(obj, event)
    
if __name__ == "__main__":
    main(sys.argv)

