#!/usr/bin/env python

import sys, random
import StringIO
import contextlib
from PyQt4 import QtCore, QtGui, QtDeclarative

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

class Messenger(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    
    def __init__(self, *args):
        QtCore.QObject.__init__(self, *args)
        with stdoutIO() as s:
            exec "import this"
        self.zen = s.getvalue().split("\n")
    
    def emit_message(self):
        with stdoutIO() as s:
            exec "import this"
        ind = random.randint(0, len(self.zen)-1)
        self.message.emit(self.zen[ind])
    
def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setSource(QtCore.QUrl("main.qml"))

    messenger = Messenger()
    root = view.rootObject()
    root.messageRequested.connect(messenger.emit_message)
    messenger.message.connect(root.updateMessage)
    root.updateMessage("Hallo Welt!")

    view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
