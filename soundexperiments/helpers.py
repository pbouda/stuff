# coding: utf-8
import wave, struct, numpy, math
from PyQt4 import QtMultimedia, QtCore

def audio_output(nchannels = 1, framerate = 9600, sampwidth = 2):
    format = QtMultimedia.QAudioFormat()
    format.setChannels(nchannels)
    format.setFrequency(framerate)
    format.setSampleSize(sampwidth * 8)
    format.setCodec("audio/pcm")
    format.setByteOrder(QtMultimedia.QAudioFormat.LittleEndian)
    format.setSampleType(QtMultimedia.QAudioFormat.SignedInt)
    output = QtMultimedia.QAudioOutput(format)
    return output

def audio_output_from_wave_file(filename):
    sound = wave.open(filename)
    (nchannels, sampwidth, framerate, _, _, _) = sound.getparams()
    return audio_output(nchannels, framerate, sampwidth)

def bytarray_from_numpyarray(arr, pack_format):
    ba = QtCore.QByteArray()
    for s in arr:
        s_int = int(s*math.pow(2, 15))
        ba.append(struct.pack(pack_format, s_int))
    return ba

def numpyarray_from_wave_file(filename):
    sound = wave.open(filename)
    (nchannels, sampwidth, framerate, nframes, _, _) = sound.getparams()
    samples = numpy.zeros(nframes, dtype=float)
    for i in range(nframes):
        f = sound.readframes(1)
        sample = struct.unpack("<h", f)
        s = float(sample[0] / math.pow(2, 15))
        samples[i] = s
    return samples
 