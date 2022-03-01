from kivy.uix.widget import Widget
from kivymd.uix.label import MDIcon
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line,Color,Rectangle
from kivy.app import App
import app.settings
from kivy.metrics import dp
from uuid import uuid1
import app.settings

class SchemaObject(RelativeLayout):
	data=None
	moving=False
	pinned=False
	bgcol=None
	z=None

	def __getstate__(self):
		return self.data['uuid'].hex
		
	def __setstate__(self,state):
		self.toresolve=state
		app.settings.toresolv.append(self)
	
	def savelayout(self):
		if self.data:
			self.data['size']=(self.size[0]/dp(1),self.size[1]/dp(1))
			self.data['pos']=(self.pos[0]/dp(1),self.pos[1]/dp(1))
		
	def redraw(self,*args):
		if self.pinned:
			if not self.r:
				self.canvas.before.add(Color(self.bgcolor))
			else:
				self.canvas.before.remove(self.r)
			self.r=Rectangle(pos=(0,0),size=self.size)
			self.canvas.before.add(self.r)
		self.savelayout()
		
	def __init__(self,data=None,**kwargs):
		super(SchemaObject,self).__init__(**kwargs)
		self.data=data
		self.pinned=False
		self.filter=False
		self.bgcolor=App.get_running_app().theme_cls.bg_normal
		self.bgcolor[3]=1.0
		if not self.data in app.settings.schema:
			if not self.data is None:
				app.settings.schema.append(self.data)
				self.data['uuid']=uuid1()
		self.r=None
		self.bind(on_touch_down=self.my_touch_down,
                  on_touch_move=self.my_touch_move, on_touch_up=self.my_touch_up)

	def my_touch_down(self,object,touch):
		if not object.pinned and not object.filter:
			f=None
			for i in object.walk(restrict=True):
				if not i is object:
					if i.collide_point(*i.to_widget(*touch.pos)):
						f=i
			if f:
				if type(f) is MDIcon:
					object.moving=True
					return True
				else:
					if not hasattr(f,'on_touch'):
						return True
					else:
						return f.on_touch(touch)
			else:
				return(True)
		else:
			return True
		
	def my_touch_move(self,object,touch):
		if object.moving:
			object.pos=touch.pos
			for i in object.parent.walk(restrict=True):
				if i.collide_point(*touch.pos) and not i is object and not i is object.parent and hasattr(i,'collide'):
					self.z=i
					i.collide(object,touch)
			return True
		else:
			return object.on_touch_move(touch)
	
	def my_touch_up(self,object,touch):
		if object.moving:
			object.moving=False
			return True
		else:
			return object.on_touch_up(touch)