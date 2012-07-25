from math import pi, sin
import struct, sys

from PyQt4.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PyQt4.QtGui import QApplication, QFormLayout, QLineEdit, QHBoxLayout, \
                        QPushButton, QSlider, QVBoxLayout, QWidget
from PyQt4.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput

class Window(QWidget):

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        format = QAudioFormat()
        format.setChannels(1)
        format.setFrequency(22050)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        self.output = QAudioOutput(format, self)
        
        self.frequency = 440
        self.volume = 0
        self.buffer = QBuffer()
        self.data = QByteArray()
        
        self.deviceLineEdit = QLineEdit()
        self.deviceLineEdit.setReadOnly(True)
        self.deviceLineEdit.setText(QAudioDeviceInfo.defaultOutputDevice().deviceName())
        
        self.pitchSlider = QSlider(Qt.Horizontal)
        self.pitchSlider.setMaximum(100)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximum(32767)
        self.volumeSlider.setPageStep(1024)
        
        self.playButton = QPushButton(self.tr("&Play"))
        
        self.pitchSlider.valueChanged.connect(self.changeFrequency)
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.playButton.clicked.connect(self.play)
        
        formLayout = QFormLayout()
        formLayout.addRow(self.tr("Device:"), self.deviceLineEdit)
        formLayout.addRow(self.tr("P&itch:"), self.pitchSlider)
        formLayout.addRow(self.tr("&Volume:"), self.volumeSlider)
        
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addStretch()
        
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.addLayout(formLayout)
        horizontalLayout.addLayout(buttonLayout)
    
    def changeFrequency(self, value):
    
        self.frequency = 440 + (value * 2)
    
    def play(self):
    
        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
        
        if self.buffer.isOpen():
            self.buffer.close()
        
        self.createData()
        
        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        
        self.output.start(self.buffer)
    
    def changeVolume(self, value):
    
        self.volume = value
    
    def createData(self):
    
        # Create 2 seconds of data with 22050 samples per second, each sample
        # being 16 bits (2 bytes).
        
        self.data.clear()
        for i in xrange(2 * 22050):
            t = i / 22050.0
            value = int(self.volume * sin(2 * pi * self.frequency * t))
            self.data.append(struct.pack("<h", value))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())