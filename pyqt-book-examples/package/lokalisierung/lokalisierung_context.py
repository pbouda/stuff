# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

class A(QtCore.QObject):
    def hello(self):
        return self.tr("Hello")

class B(A):
    pass

app = QtGui.QApplication(sys.argv)
language = unicode(QtCore.QLocale.system().name())
myappTranslator = QtCore.QTranslator()
myappTranslator.load("lokalisierung_context_{0}".format(language))
app.installTranslator(myappTranslator)

a = A()
print a.hello()

b = B()
print b.hello()