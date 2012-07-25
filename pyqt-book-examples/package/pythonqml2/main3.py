# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os, traceback
from PySide import QtCore, QtGui, QtDeclarative

utterances = []
utterances.append({
    "id": "a1",
    
    "utterance":
        u"dün ak\u015Fam ko\u015Fa ko\u015Fa eve geldim",
        
    "ilelements":    
        [ [u'dün', u'dün', u'yesterday'],
          [u'ak\u015Fam', u'ak\u015Fam', u'evening'],
          [u'ko\u015Fa', u'ko\u015F-a', u'run-CV'],
          [u'ko\u015Fa', u'ko\u015F-a', u'run-CV'],
          [u'eve', u'ev-e', u'home-DIR'],
          [u'geldim', u'gel-di-m', u'come-PAST-1SG']
        ],
    
    "translations":
        [ u"yesterday evening I came home running" ]
})

def main(argv):
    app = QtGui.QApplication(argv)
    view = QtDeclarative.QDeclarativeView()
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeViewToRootObject)
    
    context = view.rootContext()
    context.setContextProperty("utterances", utterances)

    view.setSource(QtCore.QUrl("main3.qml"))
    view.resize(480, 120)
    view.show()
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
