from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle,Color,Line,Triangle
from  kivy.metrics import dp

import commons

from uuid import uuid4

class ProxyStackLayout(StackLayout):
	
	def count_height(self):
	    h=0
	    l=None
	    prevy=0
	    for i in self.walk(restrict=True):
	        if isinstance(i,RelativeLayout):
	           if i.y != prevy:
		           l=i
		           h=h+i.height+dp(2)
		           prevy=i.y
	    return h,l
	    
	def count_width(self,widget):
		w=0
		for i in self.walk(restrict=True):
			if isinstance(i,RelativeLayout):
				if i.width>w:
					w=i.width
		return w
	
	def layout(self,widget):
		c,l=self.count_height()
		if l:
			if l.width + widget.width > self.width:
				c = c+widget.height+dp(2)
		if c >= self.parent.height:
		    self.parent.height=c+dp(2)
		    self.parent.parent.height=c+self.parent.parent._title.height
		w=self.count_width(widget)
		if w>self.width:
			self.parent.parent.width=w+dp(2)
		self.parent.parent._trigger()
	
	def theme_primary_color(self):
		return self.parent.parent.parent.theme_primary_color()
		
	def bg_color(self):
		return self.parent.parent.parent.bg_color()
		
	def primary_color_light(self):
		return self.parent.parent.parent.primary_color_light()
		
	def get_panel_canvas(self):
		return self.parent.parent.parent.canvas
		
	def __init__(self,**kwargs):
		super(ProxyStackLayout,self).__init__(**kwargs)
	
class GroupNode(RelativeLayout):
	
	title=StringProperty('')
	id=StringProperty("")
	
	def serialize(self):
		ret={}
		ret['id']=self.id
		ret['title']=self.title
		ret['members']=[]
		ret['pos']=(self.pos[0]/dp(1),self.pos[1]/dp(1))
		ret['size']=(self.size[0]/dp(1),self.size[1]/dp(1))
		for i in self._content.walk(restrict=True):
			if isinstance(i,RelativeLayout):
				ret['members'].append(str(i.id))
		return ret	
	
	def on_title(self,instance,value):
		self._title.text=value
		self._trigger()
		return True

	def layout(self,*args):
		if self.parent:
			self._title.color=self.parent.theme_primary_color()
			
	def draw(self,*args):
		if self.canvas and self.parent:
			self.layout()
			self.canvas.before.remove(self.parent.bg_color())
			if self.main_background:
				self.canvas.before.remove(self.main_background)
			self.main_background=Rectangle(pos=(0,0),size=self.size)
			self.canvas.before.add(self.parent.bg_color())
			self.canvas.before.add(self.main_background)
			if self.forecolor:
				self.canvas.before.remove(self.forecolor)
			self.forecolor=self.parent.primary_color_light()
			self.canvas.before.add(self.forecolor)
			if self.outline:
				self.canvas.before.remove(self.outline)
			self.outline=Line(points=[0,0,self.size[0],0,self.size[0],self.size[1],0,self.size[1],0,0])
			self.canvas.before.add(self.outline)
			for i in self.parent.walk(restrict=True):
				if not i is self and isinstance(i,RelativeLayout):
					i._trigger()
			
	def on_size(self,*args):
		self.draw()
		
	def on_pos(self,*args):
		self.draw()
		
	def in_handle(self,touch):
		i=self.to_widget(*touch.pos)
		if self._title.collide_point(*i):
				return True
		return False
		
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			if self.in_handle(touch):
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
			
	def on_parent(self,instance,p):
		if p is None:
			commons.schema.remove(self)
		else:
			if not self in commons.schema:
				commons.schema.append(self)
	
	def __init__(self,id=None,title='Untitled Group',**kwargs):
		self._trigger=Clock.create_trigger(self.draw)
		super(GroupNode,self).__init__(**kwargs)
		if not id:
			self.id=str(uuid4())
		else:
			self.id=id
		self._root=BoxLayout(orientation='vertical',size_hint=(1,1))
		self.main_background=None
		self.forecolor=None
		self.outline=None
		self.moving=False
		self._title=Label(text=self.title,size_hint=(1,0.2))
		self._root.add_widget(self._title)
		self.title=title
		self._content=ProxyStackLayout(orientation='lr-tb',size_hint=(1,0.8))
		self._root.add_widget(self._content)
		self.add_widget(self._root)
		commons.schema.append(self)
