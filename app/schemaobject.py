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
		if hasattr(self,'moving'):
			if hasattr(self,'menuvisible'):
				if self.moving and self.menuvisible:
					self.menuvisible=False
					self.parent.remove_widget(self.m)
		self.savelayout()
		
	def __init__(self,data=None,**kwargs):
		super(SchemaObject,self).__init__(**kwargs)
		self.data=data
		self.pinned=False
		self.filter=False
		self.bgcolor=App.get_running_app().theme_cls.bg_normal
		if not self.data in app.settings.schema:
			if not self.data is None:
				app.settings.schema.append(self.data)
				self.data['uuid']=uuid1()
		self.r=None

	def my_touch_down(self,object,touch):
		if not object.pinned and not object.filter:
			for i in object.walk(restrict=True):
				if not i is object and i.collide_point(*i.to_widget(*touch.pos)):
					zzf="SchemaGroup" in str(type(i.parent))
					if isinstance(i,MDIcon) and not zzf:
						object.moving=True
						object.pos=touch.pos
					else:
						print('titi')
						object.moving=False
						if zzf:
							return True
						else:
							return i.on_touch_down(touch)
			return True
		else:
			print("Pinned")
		
	def my_touch_move(self,object,touch):
		if object.moving:
			object.pos=touch.pos
			for i in object.parent.walk(restrict=True):
				if i.collide_point(*touch.pos) and not i is object and not i is object.parent and hasattr(i,'collide'):
					i.collide(object,touch)
			return True
		else:
			return True
	
	def my_touch_up(self,object,touch):
		if object.moving:
			object.pos=touch.pos
			object.moving=False
			return True
		else:
			return True