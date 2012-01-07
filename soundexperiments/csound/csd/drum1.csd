<CsoundSynthesizer>

<CsOptions>
</CsOptions>

<CsInstruments>
sr      =        44100                      ; Sample rate
kr      =        44100                      ; Kontrol rate
ksmps   =        1                          ; Samples/Kontrol period
nchnls  =        2                          ; Normal stereo

;---------------------------------------------------------
; Formant pop
;---------------------------------------------------------
       instr     10

idur   =         p3            ; Duration
iamp   =         p4            ; Amplitude
ifqc   =         cpspch(p5)
ipanl  =         sqrt(p6)      ; Pan left
ipanr  =         sqrt(1-p6)    ; Pan right
if1    =         p7*ifqc       ; Formant fqc 1
ia1    =         p8            ; Formant amp 1
iwdth  =         p9*.1         ; Band width

adclck linseg    0, .002, 1, idur-.004, 1, .002, 0 ; Declick envelope
kamp   linseg    0, .001, 1, .002, 0, idur-.003, 0

arnd   rand      kamp*6/iwdth                      ; Genrate impulse
asig   butterbp  arnd, ifqc, ifqc*iwdth            ; Band pass filter
asig1  butterbp  arnd, if1,  if1*iwdth             ; Band pass filter

aout   =         (asig+asig1*ia1)*iamp*adclck      ; Apply amp envelope and declick

       outs      aout*ipanl, aout*ipanr            ; Output the sound

       endin

;---------------------------------------------------------
; Kick Drum
;---------------------------------------------------------
       instr     11

idur   =         p3            ; Duration
iamp   =         p4            ; Amplitude
iacc   =         p5            ; Accent
irez   =         p6            ; Resonance
iod    =         p7            ; Overdrive
ilowf  =         p8            ; Low Frequency

kfenv  linseg    1000*iacc,  .02, 180, .04, 120, idur-.06, ilowf ; Freq Envelope
kaenv  expseg    .1, .001, 1, .02, 1, .04, .7, idur-.062, .7  ; Amp Envelope
kdclck linseg    0, .002, 1, idur-.042, 1, .04, 0             ; Declick
asig   rand      2                                            ; Random number

aflt   rezzy     asig, kfenv, irez*40         ; Filter

aout1  =         aflt*kaenv*3*iod/iacc        ; Scale the sound

krms   rms       aout1, 1000                  ; Limiter, get rms
klim   table3    krms*.5, 5, 1                ; Get limiting value
aout   =         aout1*klim*iamp*kdclck/sqrt(iod)*1.3   ; Scale again and ouput

       outs      aout, aout                   ; Output the sound

       endin

;---------------------------------------------------------
; FM Tom-Tom
;---------------------------------------------------------
       instr     12

idur   =         p3            ; Duration
iamp   =         p4            ; Amplitude
ifqc   =         cpspch(p5)    ; Convert pitch to frequency
irez   =         p6            ; Resonance or Q
ifco   =         p7            ; Cut off frequency
ihit   =         p8            ; Noise duration
ihamp  =         p9            ; Noise amplitude
ipanl  =         sqrt(p10)     ; Pan left
ipanr  =         sqrt(1-p10)   ; Pan right

afqc1  linseg    1+iamp/30000, ihit*.5*idur, 1, .1, 1 ; Pitch bend
afqc   =         afqc1*afqc1                       ; Pitch bend squared
adclck linseg    0, .002, 1, idur-.004, 1, .002, 0 ; Declick envelope
aamp1  expseg    .01, .001, 1, idur-.001, .04      ; Tone envelope
aamp2  expseg    .01, .001, 1, idur*ihit-.001, .01 ; Noise envelope

arnd1  rand      ihamp                          ; Genrate noise
arnd   rezzy     arnd1, ifco, irez, 1           ; High pass mode
asig   oscil     1, afqc*ifqc*(1+arnd*aamp2), 1 ; Frequency modulation with noise

aout   =         asig*iamp*aamp1*adclck         ; Apply amp envelope and declick

       outs      aout*ipanl, aout*ipanr         ; Output the sound

       endin

</CsInstruments>       

<CsScore>
f1 0 65536 10 1
f5 0 1024 -8 1 256 1 256 .5 128 .3 128 .1 256 .1

; Formant pop
;    Sta     Dur  Amp    Pitch  Pan  FrmFqc  FrmAmp  BW
i10  0.000   .15  25000  7.00   .5   4       .6      .18
i10  0.250   .15  18000  7.04   .9   3.5     .8      .18
i10  0.500   .15  25000  7.00   .7   4       .6      .16
i10  0.750   .15  25000  7.00   .3   4       .6      .17

i10  0.750   .25  0      7.00   .5   2       .6      2
s

i10  0.000   .15  25000  7.00   .5   1       .6      .13
i10  0.125   .15  25000  7.04   .1   1.5     .6      .18
i10  0.375   .15  25000  7.04   .8   6       .6      .18
i10  0.500   .15  25000  7.00   .7   2       .6      .16
i10  0.625   .15  20000  7.07   .2   3       .6      .18
i10  0.750   .15  25000  7.00   .3   4       .6      .17

i10  0.750   .25  0      7.00   .5   2       .6      2
s

f5 0 1024 -8 1 256 1 256 .5 128 .3 128 .1 256 .1

; Techno Bass Drum
r3
;    Sta   Dur  Amp    Accent  Q    Overdrive  LowFqc
i11  0.0   .18  30000  1.2     1    2          60
i11  0.5   .    .      1       <    2.5        .
i11  1.0   .    .      .       <    2          80
i11  1.5   .2   .      .       1.5  3          40
f0 2
s
i11  0.0   .18  30000  1       1    2          60
i11  0.5   .    .      .       <    2.5        .
i11  1.0   .    .      .       <    2          .
i11  1.5   .    .      .       <    2          80
i11  1.75  .25  .      .       1.5  3          60

r3
;    Sta   Dur  Amp    Accent  Q    Overdrive  LowFqc
i11  0.0   .18  30000  1.2     1    2          60
i11  0.5   .    .      1       <    2.5        .
i11  1.0   .    .      .       <    2          80
i11  1.5   .2   .      .       1.5  3          40
f0 2
s
i11  0.0   .18  30000  1       1    2          60
i11  0.5   .    .      .       <    2.5        .
i11  1.0   .    .      .       <    2          .
i11  1.5   .    .      .       <    2          80
i11  1.75  .25  .      .       1.5  3          60
s

; FM Tom-Toms
;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.125   .13  23000  6.09   30  1200  .18    70      .2
i12  0.250   .15  25000  6.09   20  300   .22    40      .5
i12  0.500   .15  25000  6.09   20  600   .22    70      .4
i12  0.750   .25  29000  7.02   30  900   .11    95      .8

i12  0.00    1    0      6.09   20  500   .7     100     .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.125   .13  23000  6.09   30  1200  .18    30      .2
i12  0.250   .15  25000  6.09   20  300   .22    40      .5
i12  0.500   .12  21000  6.09   20  600   .22    30      .4
i12  0.750   .25  29000  6.07   30  900   .11    95      .8

i12  0.00    1    0      6.09   20  500   .7     100     .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.125   .13  23000  6.10   10  1200  .18    20      .2
i12  0.250   .15  25000  6.09   60  2300  .72    10      .5
i12  0.375   .17  23000  6.10   10  1400  .25    20      .8
i12  0.500   .15  25000  6.09   60  2600  .72    10      .4
i12  0.750   .25  29000  7.02   30  900   .11    95      .8

i12  0.00    1    0      6.09   20  500   .7     100     .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.000   .18  20000  7.01   20  400   .23    40      .9
i12  0.125   .13  23000  6.09   30  1200  .18    70      .2
i12  0.250   .15  25000  6.09   20  300   .22    40      .5
i12  0.375   .17  23000  6.10   10  1400  .25    40      .8
i12  0.500   .15  25000  6.09   20  600   .22    70      .4
i12  0.625   .12  20000  6.10   10  1000  .25    50      .5
i12  0.750   .25  29000  6.07   30  900   .11    95      .8

i12  0.00  1    0      6.09   20  500   .7     100       .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.125   .13  23000  6.09   30  1200  .18    70      .2
i12  0.250   .19  25000  6.09   20  300   .22    40      .0
i12  0.375   .13  23000  6.10   30  1400  .35    20      .8
i12  0.500   .19  25000  6.09   40  3600  .32    20      .4
i12  0.625   .12  20000  6.10   10  1000  .25    50      .99
i12  0.750   .19  29000  6.07   30  900   .11    95      .8
i12  0.875   .11  20000  7.02   10  1000  .25    30      .4

i12  0.00  1    0      6.09   20  500   .7     100       .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.000   .18  20000  7.02   20  400   .23    40      .9
i12  0.125   .13  23000  6.09   30  1200  .18    30      .2
i12  0.250   .19  25000  6.09   20  300   .22    40      .1
i12  0.375   .13  23000  6.10   10  1400  .25    40      .8
i12  0.500   .19  25000  6.07   20  600   .22    30      .4
i12  0.750   .25  29000  6.10   30  900   .11    95      .8

i12  0.00  1    0      6.09   20  500   .7     100       .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.125   .13  23000  6.09   30  1200  .18    70      .2
i12  0.250   .19  25000  6.09   20  300   .22    40      .5
i12  0.375   .13  23000  6.10   30  1400  .35    20      .8
i12  0.500   .19  25000  6.09   40  3600  .32    20      .1
i12  0.625   .12  20000  6.10   10  1000  .25    50      .5
i12  0.750   .19  29000  6.07   30  900   .11    95      .8
i12  0.875   .11  20000  7.02   10  1000  .25    30      .4

i12  0.00  1    0      6.09   20  500   .7     100       .5
s

;    Sta     Dur  Amp    Pitch  Q   Fqc   HitDur HitAmp  Pan
i12  0.000   .18  20000  7.02   20  400   .23    40      .9
i12  0.125   .13  23000  6.09   40  3200  .68    10      .2
i12  0.250   .19  25000  6.09   20  300   .22    40      .5
i12  0.375   .13  23000  6.10   40  3400  .65    10      .8
i12  0.500   .26  25000  6.07   20  600   .08    90      .4
i12  0.752   .43  25000  6.09   30  900   .08    85      .0
i12  0.745   .45  25000  6.07   30  900   .08    85      .99

i12  0.00  1    0      6.09   20  500   .7     100       .5

</CsScore>

</CsoundSynthesizer>
<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>1080</x>
 <y>72</y>
 <width>198</width>
 <height>622</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>231</r>
  <g>46</g>
  <b>255</b>
 </bgcolor>
 <bsbObject version="2" type="BSBVSlider">
  <objectName>slider1</objectName>
  <x>5</x>
  <y>5</y>
  <width>20</width>
  <height>100</height>
  <uuid>{d29b1a7e-89b0-4540-b672-4f4a185e193d}</uuid>
  <visible>true</visible>
  <midichan>0</midichan>
  <midicc>-3</midicc>
  <minimum>0.00000000</minimum>
  <maximum>1.00000000</maximum>
  <value>0.00000000</value>
  <mode>lin</mode>
  <mouseControl act="jump">continuous</mouseControl>
  <resolution>-1.00000000</resolution>
  <randomizable group="0">false</randomizable>
 </bsbObject>
</bsbPanel>
<bsbPresets>
</bsbPresets>
<MacGUI>
ioView nobackground {59367, 11822, 65535}
ioSlider {5, 5} {20, 100} 0.000000 1.000000 0.000000 slider1
</MacGUI>
