from math import *

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import *

def random(v1, v2):
    import random
    start = min(v1, v2)
    end = max(v1, v2) + 1
    return int(start + random.random() * (end-start))


def coordinates(x0, y0, distance, angle):
    x1 = x0 + cos(radians(angle)) * distance
    y1 = y0 + sin(radians(angle)) * distance
    return x1, y1

class TestApp(App):
    def brushpaint(self, canvas, center=(400,300), points=10000, length=100, diminish=10):
        angle_step = 360.0 / points
        for p in range(points):
            angle = int(p*angle_step)
            x = 0; y = 0
            dx, dy = coordinates(x, y, length, angle)
            x += center[0]; y += center[1]; dx += center[0]; dy += center[1]
            with self.root.canvas:
                Bezier(points=[x,y,
                    x + random(-diminish, diminish), y + random(-diminish, diminish),
                    dx + random(-diminish, diminish), dy + random(-diminish, diminish),
                    dx, dy
                ])

    def build(self):
        self.button = Button(text='Hello World')
        self.button.bind(on_press=self.brushpaint)
        return self.button

TestApp().run()