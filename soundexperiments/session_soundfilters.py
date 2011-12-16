# coding: utf-8
from PyQt4 import QtCore, QtGui, QtMultimedia
import wave, struct, numpy, os

sound = wave.open("test.wav")
(nchannels, sampwidth, framerate, nframes, _, _) = sound.getparams()
samples = numpy.zeros(nframes, dtype=int)
for i in range(nframes):
    f = sound.readframes(1)
    sample = struct.unpack("<H", f)
    samples[i] = sample[0]

format = QtMultimedia.QAudioFormat()
format.setChannels(nchannels)
format.setFrequency(framerate)
format.setSampleSize(sampwidth * 8)
format.setCodec("audio/pcm")
format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
format.setSampleType(QtMultimedia.QAudioFormat.SignedInt)
output = QtMultimedia.QAudioOutput(format)
    
ba = QtCore.QByteArray()
for s in samples:
    ba.append(struct.pack("<H",s))

buff = QtCore.QBuffer(ba)
buff.open(QtCore.QIODevice.ReadOnly)

from scipy.signal import lfilter
a = [ 2 ]
b = [ 1, 0.75 ]
filtered_samples = lfilter(b, a, samples)

ba2 = QtCore.QByteArray()
for s in filtered_samples:
    ba2.append(struct.pack("<H", int(s)))
    
buff2 = QtCore.QBuffer(ba2)
buff2.open(QtCore.QIODevice.ReadOnly)
