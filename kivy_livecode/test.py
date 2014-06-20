from math import *

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import *


def random(v1=None, v2=None):
    """Returns a random value.
    
    This function does a lot of things depending on the parameters:
    - If one or more floats is given, the random value will be a float.
    - If all values are ints, the random value will be an integer.
    
    - If one value is given, random returns a value from 0 to the given value.
      This value is not inclusive.
    - If two values are given, random returns a value between the two; if two
      integers are given, the two boundaries are inclusive.
    """
    import random
    if v1 != None and v2 == None: # One value means 0 -> v1
        if isinstance(v1, float):
            return random.random() * v1
        else:
            return int(random.random() * v1)
    elif v1 != None and v2 != None: # v1 -> v2
        if isinstance(v1, float) or isinstance(v2, float):
            start = min(v1, v2)
            end = max(v1, v2)
            return start + random.random() * (end-start)
        else:
            start = min(v1, v2)
            end = max(v1, v2) + 1
            return int(start + random.random() * (end-start))
    else: # No values means 0.0 -> 1.0
        return random.random()


def coordinates(x0, y0, distance, angle):
    x1 = x0 + cos(radians(angle)) * distance
    y1 = y0 + sin(radians(angle)) * distance
    return x1, y1


def gradient(colors, steps):
    colors_per_step = steps / len(colors)
    num_colors = int(colors_per_step) * len(colors)
    gradient = []
    for i, color in enumerate(colors):
        # start color...
        r1 = color[0]
        g1 = color[1]
        b1 = color[2]
 
        # end color...
        color2 = colors[(i + 1) % len(colors)]
        r2 = color2[0]
        g2 = color2[1]
        b2 = color2[2]
 
        # generate a gradient of one step from color to color:
        delta = 1.0 / colors_per_step
        for j in range(int(colors_per_step)):
            t = j * delta
            a = 1.0
            r = (1.0 - t) * r1 + t * r2
            g = (1.0 - t) * g1 + t * g2
            b = (1.0 - t) * b1 + t * b2
            gradient.append([r, g, b])
 
    return gradient

class TestApp(App):

    def composeimage(self, canvas, center=(400,300), radius=200, points=100, diminish=10,
            colors = [ [0.0, 0.0, 0.0, 1.0], [0.4, 0.4, 0.4, 1.0], [1.0, 1.0, 1.0, 1.0] ]):
        count = int( radius * 1.3 )
        grad = gradient(colors, count)
        angle = 0.0
        for i in range(len(grad)):
            c = grad[i]
            with self.root.canvas:
                Color(c[0], c[1], c[2])

            #a = 0.75 - 0.25 * float( i ) / count
            self.brushpaint(canvas, center = center, points = int(points-i*0.2),
                length = radius - i + random( count - i ) / 3, diminish = diminish)

    def brushpaint(self, canvas, center=(400,300), points=100, length=100, diminish=10):
        if points <= 0 or length <= 0:
            return
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
        self.button.bind(on_press=self.composeimage)
        return self.button

TestApp().run()