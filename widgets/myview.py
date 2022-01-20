from kivy.graphics import Color, RoundedRectangle
from widgets.mylabel import MyLabel
from kivy.uix.widget import Widget
from kivy.metrics import dp

class MyView(Widget):

	def layout(self):
		self.title.pos=(self.pos[0]+10,self.pos[1]+self.size[1]-self.title.texture_size[1]-10)
		self.content.size=(self.size[0]-20, self.size[1] - self.title.texture_size[1]-20)
		self.content.pos=(self.pos[0]+10,self.pos[1]+10)
		
	def __init__(self,viewtitle=None,content=None,**kwargs):
		super(MyView,self).__init__(**kwargs)
		self.data=content
		self.size_hint=(None,None) 
		self.title=MyLabel(text=viewtitle,font_size=14)
		self.title.texture_update()
		self.content=content.geteditor(size=(self.size[0]-20, self.size[1] - self.title.texture_size[1]-20),pos=(self.pos[0]+10,self.pos[1]+10))
		self.add_widget(self.title)
		self.add_widget(self.content)
		self.layout()
		self.bind(pos=self.redraw,size=self.redraw)
		self.redraw()

	def redraw(self,*args):
		self.layout()
		self.canvas.before.clear()
		with self.canvas.before:
			Color(0.2, 0.2, 0.2, 0.3)
			RoundedRectangle(pos=self.pos,size=self.size,radius=[(10,10),(10,10),(10,10),(10,10)])
