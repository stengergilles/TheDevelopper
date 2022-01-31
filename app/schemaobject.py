from kivy.uix.widget import Widget

class SchemaObject(Widget):
	data=None
	content=None
	moving=False
	
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
		self.moving=True
		return super(SchemaObject, self).on_touch_down(touch)
		
	def on_touch_move(self,touch):
		if self.moving:
			self.content.pos=touch.pos
		return super(SchemaObject,self).on_touch_move(touch)
	
	def on_touch_up(self,touch):
		self.moving=False
		return super(SchemaObject,self).on_touch_up(touch)