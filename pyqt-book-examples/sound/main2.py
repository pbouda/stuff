# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import wave
from PyQt4 import QtCore, QtGui, QtMultimedia

def main(argv):
    app = QtGui.QApplication(argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    
class MainWindow(QtGui.QWidget):
    
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        
        self.createComponents()
        self.createLayout()
        self.createConnects()
        self.createAudioPlayer()
        self.setWindowTitle("Audio Player")

    def createComponents(self):
        self.buttonStart = QtGui.QPushButton(self.tr("Start"), self)
        self.buttonStop = QtGui.QPushButton(self.tr("Stop"), self)

    def createLayout(self):
        layoutCentral = QtGui.QHBoxLayout()

        layoutCentral.addWidget(self.buttonStart)
        layoutCentral.addWidget(self.buttonStop)

        self.setLayout(layoutCentral)
        
    def createConnects(self):
        self.buttonStart.clicked.connect(self.play)
        self.buttonStop.clicked.connect(self.stop)
        
    def createAudioPlayer(self):
        sound = wave.open("test.wav")
        (nchannels,
         sampwidth,
         framerate,
         nframes,
         _, _) = sound.getparams()
        
        format = QtMultimedia.QAudioFormat()
        format.setChannels(nchannels)
        format.setFrequency(framerate)
        format.setSampleSize(sampwidth * 8)
        format.setCodec("audio/pcm")
        format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
        format.setSampleType(QtMultimedia.QAudioFormat.SignedInt)
        
        self.output = QtMultimedia.QAudioOutput(format)

        self.buffer = QtCore.QBuffer()
        self.buffer.setData(sound.readframes(nframes))

    @QtCore.pyqtSlot()
    def play(self):
        self.stop()

        self.buffer.open(QtCore.QIODevice.ReadOnly)
        self.buffer.seek(0)
        self.output.start(self.buffer)
        
    @QtCore.pyqtSlot()
    def stop(self):
        if self.output.state() == QtMultimedia.QAudio.ActiveState:
            self.output.stop()
        
        if self.buffer.isOpen():
            self.buffer.close()
    
if __name__ == "__main__":
    main(sys.argv)
