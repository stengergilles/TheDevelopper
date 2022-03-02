from enum import Enum
from app.schemaobject import SchemaObject
from kivy.graphics import Line,Color,Rectangle
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
			src=self.data['src'].to_parent(self.data['src'].c.center_x,self.data['src'].c.center_y)
			dst=self.data['dst'].to_parent(self.data['dst'].c.center_x,self.data['dst'].c.center_y)
			if src[0] < dst[0]:
				if src[1] < dst[1]:
					self.pos=src
					self.size=(dst[0] - src[0],dst[1] - src[1])
					src=(0,0)
					dst=self.size
				else:
					self.pos=(src[0],dst[1])
					self.size=(dst[0]-src[0],src[1]-dst[1])
					src=(self.size[0],0)
					dst=(0,self.size[1])
			else:
				if src[1] < dst[1]: 
					self.pos=(dst[0],src[1])
					self.size=(src[0]-dst[0],dst[1]-src[1])
					src=(self.size[0],0)
					dst=(0,self.size[1])
				else:
					self.pos=dst	
					self.size=(src[0]-dst[0],src[1]-dst[1])
					src=(0,0)
					dst=self.size
			if self.l:
				self.canvas.before.remove(self.l)
			else:
				self.canvas.before.add(Color(0,0,0,1))
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