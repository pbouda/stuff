<CsoundSynthesizer>

<CsOptions>
  -d -o dac -m0
</CsOptions>

<CsInstruments>
sr     = 41000
ksmps  = 10
nchnls = 1

          instr 3                       ; p3=duration of note
k1        linen     p4, p6, p3, p7      ; p4=amp
a1        oscil     k1, p5, 1           ; p5=freq
          out       a1                  ; p6=attack time
          endin    

          instr 4
iamp      =         ampdb(p4)           ; convert decibels to linear amp
iscale    =         iamp * .333         ; scale the amp at initialization
inote     =         cpspch(p5)          ; convert octave.pitch to cps

k1        linen     iscale, p6, p3, p7  ; p4=amp

a3        oscil     k1, inote*.996, 1   ; p5=freq
a2        oscil     k1, inote*1.004, 1  ; p6=attack time
a1        oscil     k1, inote, 1        ; p7=release time

a1        =         a1+a2+a3
          out       a1
          endin
</CsInstruments>

<CsScore>
f1   0    4096 10 1      ; sine wave

;ins strt dur  amp  freq      attack    release
i4   0    1    75   8.04      0.1       0.7
i4   1    1    70   8.02      0.07      0.6
i4   2    1    75   8.00      0.05      0.5
i4   3    1    70   8.02      0.05      0.4
i4   4    1    85   8.04      0.1       0.5
i4   5    1    80   8.04      0.05      0.5
i4   6    2    90   8.04      0.03      1.
</CsScore>
</CsoundSynthesizer><bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>1720</x>
 <y>72</y>
 <width>198</width>
 <height>1022</height>
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
  <uuid>{1c622847-5445-425b-98db-726c083b48fe}</uuid>
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
<EventPanel name="" tempo="60.00000000" loop="8.00000000" x="133" y="155" width="655" height="346" visible="false" loopStart="3.55482e-316" loopEnd="2.122e-314"></EventPanel>
