from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color,Ellipse
from kivy.clock import Clock
from kivy.vector  import Vector

class CircularButton(ButtonBehavior,Widget):
	
	source=None

	def __init__(self,img=None,**kwargs):
		super(CircularButton,self).__init__(**kwargs)
		self.source=img
		self.origsize=self.size.copy()
		with self.canvas:
			Ellipse(pos=self.pos,size=self.size,source=img)

	def _resize(self):
		self.size=self.origsize
		
	def on_press(self):
		self.size=(self.size[0]*0.9,self.size[1]*0.9)
		Clock.schedule_once(lambda dt:  self._resize(),0.2)
		
	def collide_point(self,x,y):
		return Vector(x,y).distance(self.center)<=self.width/2

	def redraw(self,object,pos):
		self.canvas.before.clear()
		self.canvas.clear()
		with self.canvas.before:
			Color(1.0,1.0,1.0)
			Ellipse(pos=self.pos,size=self.size,source=self.source)
