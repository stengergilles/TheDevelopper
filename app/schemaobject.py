from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line,Color,Rectangle
from kivy.app import App
import app.settings
from kivy.metrics import dp

class SchemaObject(RelativeLayout):
	data=None
	moving=False
	pinned=False
	bgcol=None
	
	def savelayout(self):
		if self.data:
			self.data['size']=(self.size[0]/dp(1),self.size[1]/dp(1))
			self.data['pos']=(self.pos[0]/dp(1),self.pos[1]/dp(1))
		
	def redraw(self,*args):
		if self.pinned:
			with self.canvas.before:
				Color(self.bgcolor)
				Rectangle(pos=(0,0),size=self.size)
		self.savelayout()
		
	def __init__(self,data=None,**kwargs):
		super(SchemaObject,self).__init__(**kwargs)
		self.data=data
		self.bgcolor=App.get_running_app().theme_cls.bg_normal
		self.bgcolor[3]=1.0
		if not data in app.settings.schema:
			if not data is None:
				app.settings.schema.append(data)
			
	def on_touch_down(self,touch):
		if not self.pinned:
			self.moving=True
		return super(SchemaObject, self).on_touch_down(touch)
		
	def on_touch_move(self,touch):
		if self.moving:
			self.pos=touch.pos
		return super(SchemaObject,self).on_touch_move(touch)
	
	def on_touch_up(self,touch):
		self.moving=False
		return super(SchemaObject,self).on_touch_up(touch)