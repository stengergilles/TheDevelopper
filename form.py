from field import Field
from kivy.graphics import Line
from kivy.uix.boxlayout import BoxLayout

import commons

class Form(BoxLayout):
	
	def serialize(self):
		l=[]
		for i in self.walk(restrict=True):
			if type(i) is Field:
				f={}
				f[i.t.helper_text]=i.t.text
				l.append(f)
		return l
	
	def layout(self):
		w=0
		for i in self.walk(restrict=True):
			if type(i) is Field:
				if i.width>w:
					w=i.width
		self.width=w
				
	def draw(self):
		self.canvas.before.clear()
		with self.canvas.before:
			commons.mainpanel.primary_color()
			Line(points=[self.pos,(self.pos[0]+self.size[0],self.pos[1])])
		
	def on_size(self,*args):
		self.layout()
		self.draw()
		
	def on_pos(self,instance,p):
		self.pos=p
		self.layout()
		self.draw()
		return True
	
	def __init__(self,**kwargs):
		super(Form,self).__init__(**kwargs)
		self.size_hint=(None,None)
		self.orientation='vertical'
		self.count=0
	
	def add_field(self,name=None,default=None,value=None):
		if default is None:
			default="Default Value"
		z=Field(labeltext=name,defaultvalue=default)
		if value:
			z.t.text=value
		self.add_widget(z)
		self.count =self.count+1
		self.layout()
		
	def remove_field(self,name=None):
		for i in self.walk(restrict=True):
			if type(i) is Field:
				if i.t.helper_text==name:
					self.remove_widget(i)
					return True
		return False
		
	def find_field(self,name=None):
		for i in self.walk(restrict=True):
			if type(i) is Field:
				if i.t.helper_text==name:
					return i
		return None