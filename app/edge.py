from enum import Enum
from app.schemaobject import SchemaObject
from kivy.graphics import Line,Color,Rectangle,Triangle
from kivy.clock import Clock
from kivy.app import App

class direction(Enum):
	SRCDST=1
	DSTSRC=2
	BOTH=3
	NONE=4
	
class SchemaEdge(SchemaObject):
		
	def redraw(self, *args):
		if self.data['src'] and self.data['dst']:
			self.data['src'].create()
			self.data['dst'].create()
			cs=self.data['src'].c.size[0]/2
			ss=max(self.size[0],self.size[1])*0.1
			t1=None
			t2=None
			src=self.data['src'].to_parent(self.data['src'].c.center_x,self.data['src'].c.center_y)
			dst=self.data['dst'].to_parent(self.data['dst'].c.center_x,self.data['dst'].c.center_y)
			if src[0] < dst[0]:
				if src[1] < dst[1]:
					self.pos=src
					self.size=(dst[0] - src[0],dst[1] - src[1])
					src=(0,0)
					src=(src[0]+cs,src[1]+cs)
					dst=self.size
					dst=(dst[0]-cs,dst[1]-cs)
					if self.data['dir']==direction.SRCDST:
						t1=Triangle(points=[dst[0],dst[1],dst[0]-ss,dst[1],dst[0],dst[1]-ss])
					else:
						if self.data['dir']==direction.DSTSRC:
							t1=Triangle(points=[src[0],src[1],src[0],src[1]+ss,src[0]+ss,src[1]])
						else:
							if self.data['dir']==direction.BOTH:
								t1=Triangle(points=[dst[0],dst[1],dst[0]-ss,dst[1],dst[0],dst[1]-ss])
								t2=Triangle(points=[src,src[0],src[1]+ss,src[0]+ss,src[1]])
				else:
					self.pos=(src[0],dst[1])
					self.size=(dst[0]-src[0],src[1]-dst[1])
					src=(self.size[0],0)
					src=(src[0]-cs,src[1]+cs)
					dst=(0,self.size[1])
					dst=(dst[0]+cs,dst[1]-cs)
			else:
				if src[1] < dst[1]: 
					self.pos=(dst[0],src[1])
					self.size=(src[0]-dst[0],dst[1]-src[1])
					src=(self.size[0],0)
					src=(src[0]-cs,src[1]+cs)
					dst=(0,self.size[1])
					dst=(dst[0]+cs,dst[1]-cs)
				else:
					self.pos=dst	
					self.size=(src[0]-dst[0],src[1]-dst[1])
					src=(0,0)
					src=(src[0]+cs,src[1]+cs)
					dst=self.size
					dst=(dst[0]-cs,dst[1]-cs)
			if self.l:
				self.canvas.before.remove(self.l)
			else:
				self.canvas.before.add(Color(0,0,0,1))
			if self.p1:
				self.canvas.before.remove(self.p1)
				self.p1=None
			if self.p2:
				self.canvas.before.remove(self.p2)
				self.p2=None
			if t1:
				self.p1=t1
				print('add1')
				self.canvas.before.add(self.p1)
			if t2:
				self.p2=t2
				print('add2')
				self.canvas.before.add(self.p2)
			self.l=Line(points=[src,dst])
			self.canvas.before.add(self.l)
		return super().redraw(*args)
		
	def resolve(self,d=None):
		for i in App.get_running_app().panel.walk(restrict=True):
			if isinstance(i,SchemaObject):
				if d == i.data['uuid']['hex']:
					return(i)
		return(None)
	
	def __init__(self,data=None,src=None,dst=None,dir=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)
		self.l=None
		self.p1=None
		self.p2=None
		self.filter=True
		if not dir:
			data['dir']=direction.NONE
		else:
			data['dir']=dir
		data['type']=type(self)
		if 'src' in data:
			if data['src'] is None:
				data['src']=src
			else:
				data['src']=self.resolve(data['src'])
		else:
			data['src']=src
		if 'dst' in data:
			if data['dst'] is None:
				data['dst']=dst
			else:
				data['dst']=self.resolve(data['dst'])
		else:
			data['dst']=dst
		if not hasattr(data['src'],'wantlink'):
			data['src'].wantlink=[]
		data['src'].wantlink.append(data['dst'])
		if not hasattr(data['src'].wantlink[-1],'e'):
			data['src'].wantlink[-1].e=[]
		data['src'].wantlink[-1].e.append(self)
		if not hasattr(data['dst'],'wantlink'):
			data['dst'].wantlink=[]
		data['dst'].wantlink.append(data['src'])
		if not hasattr(data['dst'].wantlink[-1],'e'):
			data['src'].wantlink[-1].e=[]
		data['dst'].wantlink[-1].e.append(self)
		self.direction=dir
		self.menuvisible=False
		Clock.schedule_once(self.redraw,0.005)