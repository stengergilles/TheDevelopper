from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout

class SchemaObject(RelativeLayout):
	data=None
	content=None
	moving=False
	pinned=False
	
	def __init__(self,data=None,**kwargs):
		super(SchemaObject,self).__init__(**kwargs)
		self.data=data
		
	def on_pos(self,w,v):
		if self.content:
			self.content.pos=v
	
	def on_size(self,w,v):
		if self.content:
			self.content.size=v
			
	def on_touch_down(self,touch):
		if not self.pinned:
			self.moving=True
		return super(SchemaObject, self).on_touch_down(touch)
		
	def on_touch_move(self,touch):
		if self.moving:
			self.content.pos=touch.pos
		return super(SchemaObject,self).on_touch_move(touch)
	
	def on_touch_up(self,touch):
		self.moving=False
		return super(SchemaObject,self).on_touch_up(touch)