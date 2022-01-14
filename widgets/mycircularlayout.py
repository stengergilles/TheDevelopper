from abc import ABC

from kivy.graphics import Ellipse, Color
from kivymd.uix.circularlayout import MDCircularLayout


class MyCircularLayout(MDCircularLayout, ):

    def __init__(self, **kwargs):
        super(MyCircularLayout, self).__init__(**kwargs)
        self.bind(pos=self.redraw,size=self.redraw)
        with self.canvas.before:
            Color(1.0, 1.0, 1.0,0.3)
            Ellipse(pos=self.pos, size=self.size)

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1.0, 1.0, 1.0,0.3)
            Ellipse(pos=self.pos, size=self.size)
