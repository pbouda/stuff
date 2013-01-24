# phase vocoder example
# (c) V Lazzarini, 2010
# GNU Public License
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 
import sys
from scipy import *
from pylab import *
from scipy.io import wavfile
 
N = 2048
H = N/4
 
# read input and get the timescale factor
(sr,signalin) = wavfile.read(sys.argv[2])
L = len(signalin)
tscale = float(sys.argv[1])
 
# signal blocks for processing and output
phi  = zeros(N)
out = zeros(N, dtype=complex)
sigout = zeros(L/tscale+N)
 
# max input amp, window
amp = max(signalin)
print amp
win = hanning(N)
 
p = 0
pp = 0
while p < L-(N+H):
    # take the spectra of two consecutive windows
    p1 = int(p)
    spec1 =  fft(win*signalin[p1:p1+N])
    spec2 =  fft(win*signalin[p1+H:p1+N+H])
    # take their phase difference and integrate
    phi += (angle(spec2) - angle(spec1))
    # bring the phase back to between pi and -pi
    while any(phi) < -pi: phi += 2*pi
    while any(phi) >= pi: phi -= 2*pi
    out.real, out.imag = cos(phi), sin(phi)
    # inverse FFT and overlap-add
    sigout[pp:pp+N] += win*ifft(abs(spec2)*out)
    pp += H
    p += H*tscale
 
#  write file to output, scaling it to original amp
wavfile.write(sys.argv[3],sr,array(amp*sigout/max(sigout), dtype='int16'))

#  play it using a libsndfile utility
import pygame
pygame.mixer.init(frequency=sr, channels=1)
snd_array = array(amp*sigout/max(sigout), dtype='int16')
pygame.sndarray.make_sound(snd_array)
