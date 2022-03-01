
from app.schemaobject import SchemaObject
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel,MDIcon
from kivy.graphics import Line,Color,Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
from widget.fieldform import FieldForm
from app.edge import SchemaEdge
from app.menu import Menu
from app.edge import direction

class NodeGraph(SchemaObject):
	
	def link1(self):
		print('link1')
		s=SchemaEdge(data={},src=self.wantlink[-1],dst=self,dir=direction.SRCDST)
		self.e.append(s)
		self.wantlink[-1].e.append(s)
		self.parent.add_widget(s)	
		Clock.schedule_once(s.redraw,0.005)
		self.menuvisible=False
		self.remove_widget(self.m)
		
	def link2(self):
		s=SchemaEdge(data={},dst=self.wantlink[-1],src=self,dir=direction.DSTSRC)
		self.e.append(s)
		self.wantlink[-1].e.append(s)
		self.parent.add_widget(s)	
		Clock.schedule_once(s.redraw,0.005)
		self.menuvisible=False
		self.remove_widget(self.m)
		
	def link3(self):
		print('link3')
		self.menuvisible=False
		self.remove_widget(self.m)
		
	def link4(self):
		print('link4')
		self.menuvisible=False
		self.remove_widget(self.m)
		
	def group(self):
		print('group')
		self.menuvisible=False
		self.remove_widget(self.m)
	
	def collide(self,object,touch):
		if type(object) is NodeGraph:
			self.wantlink.append(object)
			object.wantlink.append(self)
			object.m.center_x=touch.pos[0]
			object.m.center_y=touch.pos[1]
			if not object.menuvisible:
				object.menuvisible=True
				object.parent.add_widget(object.m)
	
	def redraw(self,*args):
		super(NodeGraph,self).redraw(args)
		self.height=self.f.height+self.l.height
		self.create()
		if not self.li:
			self.canvas.before.add(Color(0,0,0))
		else:
			self.canvas.before.remove(self.li)
		self.li=Line(points=[(0,0),(self.width,0),(self.width,self.height)])
		self.canvas.before.add(self.li)
		for i in self.wantlink:
			for j in i.e:
				Clock.schedule_once(j.redraw,0.05)
			
	def create(self):
		self.li=None
		if self.data['icon']:
			i=self.data['icon']
		else:
			i='android'
		if self.data['title']:
			t=self.data['title']
		else:
			t='Untitled Node'
		if not hasattr(self,'l'):
			self.l=MDLabel(text=t,size_hint=(None,None),halign='left',font_style='Caption',pos=(dp(25),0))
			self.add_widget(self.l)
		if not hasattr(self,'c'):
			self.c=MDIcon(icon=i,pos=(0,0),size_hint=(None,None),size=(dp(24),dp(24)))
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
			self.f=FieldForm(fielddef=self.data['fieldlist'],data=self.data['fieldsvalues'],width=self.size[0]-dp(25),height=self.size[1],pos=(dp(25),self.l.height),size_hint=(None,None))
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
		Clock.schedule_once(self.redraw,0.005)