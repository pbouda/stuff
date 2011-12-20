# coding: utf-8
import numpy, math

SRATE = 9600
m = 0.001
k = 1000
r = 0.002
OVERSAMP = 50
T = 1.0 / (SRATE * OVERSAMP)
temp = (m + (T*r) + (T*T*k))
coeff1 = ((2.0*m) + (T*r)) / temp
coeff2 = -(m / temp)
Y = numpy.zeros(3, dtype=float)
Y[1] = 1.0
arr_ideal = numpy.zeros(SRATE*4, dtype=float)
arr_approx = numpy.zeros(SRATE*4, dtype=float)
for i in range(4*SRATE):
    t = float(i) / float(SRATE)
    arr_ideal[i] = math.exp(-t) * math.cos(1000.0 * t)
    for j in range(OVERSAMP):
        Y[0] = (Y[1] * coeff1) + (Y[2] * coeff2)
        Y[2] = Y[1]
        Y[1] = Y[0]
    arr_approx[i] = Y[1] - Y[2]