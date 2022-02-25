from tkinter import E
from app.schemaobject import SchemaObject
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Line,Color,Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
from widget.fieldform import FieldForm
from app.edge import SchemaEdge
from app.menu import Menu

class NodeGraph(SchemaObject):
	
	def link1(self):
		s=SchemaEdge(data={},src=self.wantlink[-1],dst=self)
		self.e.append(s)
		self.wantlink[-1].e.append(s)
		self.parent.add_widget(s)	
		Clock.schedule_once(s.redraw,0.05)
		self.menuvisible=False
		
	def link2(self):
		self.e=SchemaEdge(data={},src=self,dst=self.wantlink[-1])
		self.wantlink.e=self.e
		self.parent.add_widget(self.e)
		Clock.schedule_once(self.e.redraw,0.05)
		self.menuvisible=False
		
	def link3(self):
		print('link3')
		self.menuvisible=False
		
	def link4(self):
		print('link4')
		self.menuvisible=False
		
	def group(self):
		print('group')
		self.menuvisible=False
	
	def collide(self,object,touch):
		if type(object) is NodeGraph:
			self.wantlink.append(object)
			object.wantlink.append(self)
			self.m.center_x=touch.pos[0]
			self.m.center_y=touch.pos[1]
			if not self.menuvisible:
				self.menuvisible=True
				self.parent.add_widget(self.m)
	
	def on_size(self,*args):
		pass
	
	def redraw(self,*args):
		super(NodeGraph,self).redraw(args)
		self.create()
		c=(self.c.center_x,self.c.center_y)
#gniiii, kivy coordinates !!!!!
		self.l.pos=(self.c.width,0)
		self.l.texture_update()
		self.l.size=self.l.texture.size
		self.f.pos=(self.c.size[0],self.l.pos[1]+self.l.height+dp(1))
		if self.c.size[0] + self.f.width:
			self.width=self.c.size[0] + self.f.width
		if self.c.size[1] + self.f.height:
			self.height=self.c.size[1]+self.f.height
		with self.canvas.before:
			Color(0,0,0)
			Line(points=[c, (c[0],0),(self.width,0)])
		for i in self.wantlink:
			for j in i.e:
				Clock.schedule_once(j.redraw,0.05)
			
	def create(self):
		if self.data['icon']:
			i=self.data['icon']
		else:
			i='android'
		if self.data['title']:
			t=self.data['title']
		else:
			t='Untitled Node'
		if not hasattr(self,'l'):
			self.l=MDLabel(text=t,size_hint=(1,None),halign='left',font_style='Caption')
			self.add_widget(self.l)
		if not hasattr(self,'c'):
			self.c=MDIconButton(icon=i,pos=(0,0),size_hint=(None,None),size=(dp(16),dp(16)))
			self.add_widget(self.c)
		if not hasattr(self,'m'):
			self.m=Menu(data=[
				{
					'name':'link1',
					'icon':'arrow-left',
					'callback':self.link1
				},
				{
					'name':'link2',
					'icon':'arrow-right',
					'callback':self.link2
				},
				{
					'name':'link3',
					'icon':'arrow-all',
					'callback':self.link3
				},
				{
					'name':'link4',
					'icon':'chart-line',
					'callback':self.link4
				},
				{
					'name':'link4',
					'icon':'group',
					'callback':self.group
				}			
			])
			self.menuvisible=False
		if not hasattr(self,'f'):
			self.f=FieldForm(fielddef=self.data['fieldlist'],data=self.data['fieldsvalues'],width=self.size[0],height=self.size[1],pos=(dp(16),0),size_hint=(None,None))
			self.add_widget(self.f)
	
	def __init__(self,data=None,**kwargs):
		super(NodeGraph,self).__init__(data=data,**kwargs)
		data['fieldsvalues']={}
		data['type']=type(self)
		self.wantlink=[]
		self.e=[]
		if not 'size' in kwargs:
			self.size=(dp(100),dp(100))
		self.create()
		self.bind(pos=self.redraw,size=self.redraw)
		Clock.schedule_once(self.redraw,0.05)