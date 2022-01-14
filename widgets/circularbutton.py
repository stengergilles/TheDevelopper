from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.vector import Vector

import os

class CircularButton(ButtonBehavior, Widget):
    source = None

    def __init__(self, img=None, **kwargs):
        super(CircularButton, self).__init__(**kwargs)
        self.source = os.path.join('icons',img)
        self.origsize = self.size.copy()
        self.on_press=kwargs['on_press']
        self.bind(pos=self.redraw,size=self.redraw)
        with self.canvas:
            Ellipse(pos=self.pos, size=self.size, source=img)

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        return super().on_touch_up(touch)

    def _resize(self):
        self.size = self.origsize

    def on_press(self):
        self.size = (self.size[0] * 0.9, self.size[1] * 0.9)
        Clock.schedule_once(lambda dt: self._resize(), 0.2)
        self.on_press()

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def redraw(self, *args):
        self.canvas.before.clear()
        self.canvas.clear()
        with self.canvas.before:
            Color(1.0, 1.0, 1.0)
            Ellipse(pos=self.pos, size=self.size, source=self.source)
