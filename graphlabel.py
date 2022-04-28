from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle,Color,Line,Triangle
from kivymd.uix.label import MDIcon,MDLabel
import commons
from kivy.metrics import dp
from uuid import uuid4

class GraphLabel(RelativeLayout):
	
	title=StringProperty("")
	body=StringProperty("")
	
	def draw(self,*args):
		self.canvas.before.add(commons.mainpanel.bg_color())
		self.canvas.before.add(Rectangle(pos=(0,0),size=self.size))
		self.canvas.before.add(commons.mainpanel.primary_color())
		self.canvas.before.add(Line(points=[0,0,0,self.height,self.width,self.height,self.width,0,0,0]))
		self.canvas.before.add(Line(points=[0,self.height*0.8+dp(1),self.width,dp(1)+self.height*0.8]))
	
	def on_title(self,instance,value):
		self.t.text=value
		
	def on_body(self,instance,value):
		self.b.text=value
		
	def on_size(self,*args):
		self.draw()
		self.b.size=(self.width,self.height*0.8)
		self.b.text_size=(self.width,self.height*0.8)
	
	def edit_label(self):
		pass
		
	def in_handle(self,touch):
		i=self.to_widget(*touch.pos)
		if self.t.collide_point(*i):
				return True
		return False
		
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			if self.in_handle(touch):
				if touch.is_double_tap:
					self.edit_label()
				else:
					self.moving=True
				return True
			else:
				return False
		else:
			return False
		
	def on_touch_move(self,touch):
		if self.moving:
			self.pos=touch.pos
			return True
		else:
			return False
	
	def on_touch_up(self,touch):
		if self.moving:
			self.moving=False
			self._trigger()
			return True
		else:
			return False
			
	def __init__(self,**kwargs):
		self._trigger=Clock.create_trigger(self.draw)
		super(GraphLabel,self).__init__(**kwargs)
		if not id:
			self.id=str(uuid4())
		else:
			self.id=id
		self.size_hint=(0.3,0.3)
		self.moving=False
		l=BoxLayout(size_hint=(1,1),orientation='vertical')
		self.t=MDLabel(text="",size_hint=(1,0.2),valign='top',halign='center',theme_text_color='Custom',text_color=commons.mainpanel.theme_primary_color())
		self.b=MDLabel(text="",valign='top',text_size=(0,0),theme_text_color='Custom',text_color=commons.mainpanel.theme_primary_color())
		l.add_widget(self.t)
		l.add_widget(self.b)
		self.add_widget(l)
		commons.schema.append(self)