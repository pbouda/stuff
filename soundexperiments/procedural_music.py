# -*- coding: utf8 -*-

#http://davywybiral.blogspot.com/2010/09/procedural-music-with-pyaudio-and-numpy.html
import math
import numpy
import pyaudio
import itertools
from scipy import interpolate
from operator import itemgetter


class Note:

  NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

  def __init__(self, note, octave=4):
    self.octave = octave
    if isinstance(note, int):
      self.index = note
      self.note = Note.NOTES[note]
    elif isinstance(note, str):
      self.note = note.strip().lower()
      self.index = Note.NOTES.index(self.note)

  def transpose(self, halfsteps):
    octave_delta, note = divmod(self.index + halfsteps, 12)
    return Note(note, self.octave + octave_delta)

  def frequency(self):
    base_frequency = 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)
    return base_frequency * (2.0 ** self.octave)

  def __float__(self):
    return self.frequency()


class Scale:

  def __init__(self, root, intervals):
    self.root = Note(root.index, 0)
    self.intervals = intervals

  def get(self, index):
    intervals = self.intervals
    if index < 0:
      index = abs(index)
      intervals = reversed(self.intervals)
    intervals = itertools.cycle(self.intervals)
    note = self.root
    for i in xrange(index):
      note = note.transpose(intervals.next())
    return note

  def index(self, note):
    intervals = itertools.cycle(self.intervals)
    index = 0
    x = self.root
    while x.octave != note.octave or x.note != note.note:
      x = x.transpose(intervals.next())
      index += 1
    return index

  def transpose(self, note, interval):
    return self.get(self.index(note) + interval)


def sine(frequency, length, rate):
  length = int(length * rate)
  factor = float(frequency) * (math.pi * 2) / rate
  return numpy.sin(numpy.arange(length) * factor)

def shape(data, points, kind='slinear'):
    items = points.items()
    items.sort(key=itemgetter(0))
    keys = map(itemgetter(0), items)
    vals = map(itemgetter(1), items)
    interp = interpolate.interp1d(keys, vals, kind=kind)
    factor = 1.0 / len(data)
    shape = interp(numpy.arange(len(data)) * factor)
    return data * shape

def harmonics1(freq, length):
  a = sine(freq * 1.00, length, 44100)
  b = sine(freq * 2.00, length, 44100) * 0.5
  c = sine(freq * 4.00, length, 44100) * 0.125
  return (a + b + c) * 0.2

def harmonics2(freq, length):
  a = sine(freq * 1.00, length, 44100)
  b = sine(freq * 2.00, length, 44100) * 0.5
  return (a + b) * 0.2

def pluck1(note):
  chunk = harmonics1(note.frequency(), 2)
  return shape(chunk, {0.0: 0.0, 0.005: 1.0, 0.25: 0.5, 0.9: 0.1, 1.0:0.0})

def pluck2(note):
  chunk = harmonics2(note.frequency(), 2)
  return shape(chunk, {0.0: 0.0, 0.5:0.75, 0.8:0.4, 1.0:0.1})

def chord(n, scale):
  root = scale.get(n)
  third = scale.transpose(root, 2)
  fifth = scale.transpose(root, 4)
  return pluck1(root) + pluck1(third) + pluck1(fifth)

root = Note('A', 3)
scale = Scale(root, [2, 1, 2, 2, 1, 3, 1])

chunks = []
chunks.append(chord(21, scale))
chunks.append(chord(19, scale))
chunks.append(chord(18, scale))
chunks.append(chord(20, scale))
chunks.append(chord(21, scale))
chunks.append(chord(22, scale))
chunks.append(chord(20, scale))
chunks.append(chord(21, scale))

chunks.append(chord(21, scale) + pluck2(scale.get(38)))
chunks.append(chord(19, scale) + pluck2(scale.get(37)))
chunks.append(chord(18, scale) + pluck2(scale.get(33)))
chunks.append(chord(20, scale) + pluck2(scale.get(32)))
chunks.append(chord(21, scale) + pluck2(scale.get(31)))
chunks.append(chord(22, scale) + pluck2(scale.get(32)))
chunks.append(chord(20, scale) + pluck2(scale.get(29)))
chunks.append(chord(21, scale) + pluck2(scale.get(28)))

chunk = numpy.concatenate(chunks) * 0.25

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
stream.write(chunk.astype(numpy.float32).tostring())
stream.close()
p.terminate()