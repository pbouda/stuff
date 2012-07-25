# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui

def main(argv):
    app = QtGui.QApplication(argv)
    QtGui.QApplication.setApplicationName("HalloWelt")

    language = unicode(QtCore.QLocale.system().name())
    qtTranslator = QtCore.QTranslator()
    qtTranslator.load("qt_{0}".format(language), QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    myappTranslator = QtCore.QTranslator()
    #myappTranslator.load("lokalisierung_de")
    #language = unicode(QtCore.QLocale.languageToString(QtCore.QLocale.system().language()))
    myappTranslator.load("lokalisierung_{0}".format(language))
    app.installTranslator(myappTranslator)

    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

class MyMainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.createComponents()
        self.createLayout()

        self.setWindowTitle(self.tr("Hello World"))
        
        #status = QtGui.QMessageBox.critical(
        #    self, u"Über \"Hallo Welt\"",
        #    u"Diese Anwendung macht gar nicht.\n\
#Möchten Sie die Anwendung jetzt Schließen?",
        #    QtGui.QMessageBox.Close, QtGui.QMessageBox.Ignore)
        #if (status == QtGui.QMessageBox.Close):
        #    self.close();

    def createComponents(self):
        #self.labelHalloWelt = QtGui.QLabel(self.tr("Hello World!"))
        #self.labelHalloWelt = QtGui.QLabel(self.tr("Hello %1!").arg("World"))
        name = u"Peter"
        self.labelHalloWelt = QtGui.QLabel(self.tr("Hello {0}!").format(name))
        self.buttonTextAktualisieren = QtGui.QPushButton(self.tr("Insert"))
        self.editText = QtGui.QLineEdit()

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


