from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color,Rectangle
from kivy.metrics import dp

class MyLabel(Widget):

	def __init__(self,text=None,font_size=None,**kwargs):
		super(MyLabel,self).__init__(**kwargs)
		self.label=CoreLabel(text=text,font_size=dp(font_size))

	def texture_update(self):
		self.label.refresh()
		self.texture_size=(self.label.texture.width,self.label.texture.height)

	def on_pos(self,*args):
		self.label.refresh()
		self.size=(self.label.texture.width,self.label.texture.height)
		self.text_size=(self.label.texture.width,self.label.texture.height)
		self.canvas.before.clear()
		with self.canvas.before:
			Color(1,1,1,1)
			Rectangle(pos=(self.pos[0],self.pos[1]+5),size=self.size,texture=self.label.texture)