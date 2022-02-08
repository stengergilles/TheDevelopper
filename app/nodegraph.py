from app.schemaobject import SchemaObject
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Line,Color,Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
from widget.fieldform import FieldForm

class NodeGraph(SchemaObject):
	
	def on_size(self,*args):
		pass
	
	def redraw(self,*args):
		super(NodeGraph,self).redraw(args)
		c=(self.c.center_x,self.c.center_y)
#gniiii, kivy coordinates !!!!!
		self.f.pos=(self.c.size[0],0)
		self.f.size=(self.size[0]-self.c.size[0],self.size[1]-self.l.size[1])
		with self.canvas.before:
			Color(0,0,0)
			Line(points=[c, (c[0],self.l.pos[1]),(self.width,self.l.pos[1])])
		
	def __init__(self,data=None,**kwargs):
		super(NodeGraph,self).__init__(data=data,**kwargs)
		if not 'size' in kwargs:
			self.size=(dp(100),dp(100))
		if data['icon']:
			i=data['icon']
		else:
			i='android'
		if data['title']:
			t=data['title']
		else:
			t='Untitled Node'
		self.c=MDIconButton(icon=i,pos=(0,0),size_hint=(None,None),size=(dp(16),dp(16)))
		self.l=MDLabel(text=t,size_hint=(1,None),pos_hint={'top':1,'right':1},halign='right',font_style='Caption')
		self.f=FieldForm(fielddef=self.data['fieldlist'],width=(self.size[0]-dp(16)),height=self.size[1]-dp(16),pos=(dp(16),0),size_hint=(None,None))
		self.add_widget(self.l)
		self.add_widget(self.c)
		self.add_widget(self.f)
		self.bind(pos=self.redraw,size=self.redraw)
		Clock.schedule_once(self.redraw,0.05)
		
		