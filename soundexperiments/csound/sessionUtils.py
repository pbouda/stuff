# Copyright (C) 2010 Francois Pinot
#
# This code is free software; you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this code; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA
#

# We need to import those namespaces even
# if we import this script from a python shell
# in which they're already defined
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

def drawTable(cs, num, myflt=np.float64):
    """ftable plot"""
    buf = np.frombuffer(cs.getTableBuffer(num), myflt)
    plt.plot(buf)
    plt.axis([0, buf.size, -1.1, 1.1])

def interpolateTables(cs, num1, num2, myflt=np.float64):
    """Interpolate (num2 - num1 - 1) ftables between ftables num1 and num2"""
    buf1 = np.frombuffer(cs.getTableBuffer(num1), myflt)
    buf2 = np.frombuffer(cs.getTableBuffer(num2), myflt)
    if buf1.size != buf2.size:
        raise(ValueError("ftable %d and ftable %d don't have same length!" % (num1, num2)))
    size = buf1.size - 1
    for i in range(num1+1, num2):
        # We create a new ftable only if it doesn't
        # already exists or if it exists with a
        # different size
        if cs.TableLength(i) != size:
            cs.scoreEvent('f', [i, 0, size, 10, 0])
    dtbl = (buf2 - buf1) / (num2 - num1)
    # Wait until all pending messages are actually
    # received by the performance thread, so that
    # all new ftables are effectively created
    cs.flushMessages()
    for i in range(num1+1, num2):
        buf = np.frombuffer(cs.getTableBuffer(i), myflt)
        buf[:] = buf1 + dtbl * (i - num1)
        buf[:] /= abs(buf).max()   # normalization

def blTriangle(cs, num, size, numHarms):
    """Band limited triangle waveform"""
    h = 100.0 / np.arange(1.0, numHarms+1)
    h[1::2] = 0
    h = h * h
    h[2::4] *= -1.0
    cs.scoreEvent('f', [num, 0, size, 10] + h.tolist())
    
def blSquare(cs, num, size, numHarms):
    """Band limited square waveform"""
    h = 100.0 / np.arange(1.0, numHarms+1)
    h[1::2] = 0
    cs.scoreEvent('f', [num, 0, size, 10] + h.tolist())

def blImpulse(cs, num, size, numHarms):
    """Band limited impulse waveform"""
    h = np.ones(numHarms)
    cs.scoreEvent('f', [num, 0, size, 10] + h.tolist())

def skewlines(l1, l2, n, ax):
    ax.clear()
    ax.plot(l1[0], l1[1], l1[2], color="blue")
    ax.plot(l2[0], l2[1], l2[2], color="blue")
    tl1 = l1.transpose()
    tl2 = l2.transpose()
    sl = []
    for i in range(tl1.shape[0]):
        p1 = tl1[i]
        p2 = tl2[i]
        l = np.array([np.linspace(p1[0], p2[0], n),
                      np.linspace(p1[1], p2[1], n),
                      np.linspace(p1[2], p2[2], n)])
        ax.plot(l[0], l[1], l[2], color="red")
        sl.append(l.transpose())
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
    ax.mouse_init()
    return sl

def playHP(cs, sl, lowPitch, highPitch, duration, minFtable, maxFtable):
    nlines = len(sl)
    nelem = len(sl[0])
    dt = duration * 1.68 / nelem
    amp = 0.7 / nlines
    kpch = (highPitch - lowPitch) / 2.0
    kdur = duration / 2.0
    kftable = float(maxFtable - minFtable) / nelem  
    pmin = 10.0
    pmax = 1.0
    durList = []
    for i in range(nlines):
        durList.append(sp.randn(nelem) / 15.0 + dt)
    for i in range(nelem):
        for j in range(nlines):
            l = sl[j]
            dur = durList[j][i] + float(i) * 1.77 / nelem
            pch = (l[i][2] + 1.0) * kpch + lowPitch
            if pch < pmin:
                pmin = pch
            if pch > pmax:
                pmax = pch
            t = (l[i][1] + 1.0) * kdur
            tbl = round(i * kftable + minFtable)
            pan = (l[i][0] + 1.0) / 2.0
            cs.note([1, t, dur, amp, pch, tbl, 0.1*dur, 0.3*dur, pan])

