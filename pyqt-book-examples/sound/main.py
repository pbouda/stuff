# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PyQt4 import QtMultimedia

device = QtMultimedia.QAudioDeviceInfo.defaultOutputDevice()
info = QtMultimedia.QAudioDeviceInfo(device)
codecs = info.supportedCodecs()

print u"Device {0} unterstützt folgende Codecs:".format(device.deviceName())
for c in codecs:
    print unicode(c)

format = QtMultimedia.QAudioFormat()
format.setChannels(2)
format.setFrequency(44100)
format.setSampleSize(16)
format.setCodec("audio/pcm")
format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
format.setSampleType(QtMultimedia.QAudioFormat.SignedInt)

if device.isFormatSupported(format):
    print u"Format wird unterstützt."
else:
    print u"Format wird nicht unterstützt."