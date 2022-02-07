from kivy.uix.floatlayout import FloatLayout
from app.menu import Menu

class MainPanel(FloatLayout):
	
	def on_size(self,*args):
		for i in self.children:
			i.on_size(args)
		
	def on_touch_down(self,touch):
		for i in self.children:
			if i.collide_point(*touch.pos):
				return i.on_touch_down(touch)
		if not touch.is_double_tap:
			self.moving=True
		else:
			self.m.center_x=touch.pos[0]
			self.m.center_y=touch.pos[1]
			if not self.m.visible:
				self.m.visible=True
				self.add_widget(self.m)
		return super(MainPanel,self).on_touch_move(touch)
		
	def on_touch_move(self,touch):
		if hasattr(self,"moving"):
			if self.moving:
				for i in self.children:
					i.pos=(i.pos[0]+touch.dx,i.pos[1]+touch.dy)
				return True
		return super(MainPanel,self).on_touch_move(touch)
		
	def on_touch_up(self,touch):
		self.moving=False
		return super(MainPanel,self).on_touch_up(touch)
	
	def __init__(self,menu=None,**kwargs):
		super(MainPanel,self).__init__(**kwargs)
		self.m=Menu(data=menu,pos=(200,200))