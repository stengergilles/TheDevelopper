from enum import Enum
from app.schemaobject import SchemaObject
from kivy.graphics import Line,Color
from kivy.clock import Clock
from kivy.app import App

class direction(Enum):
	SRCDST=1
	DSTSRC=2
	BOTH=3
	NONE=4
	
class SchemaEdge(SchemaObject):
	
	def on_size(self,*args):
		pass

	def redraw(self, *args):
		if self.data['src'] and self.data['dst']:
			src=self.data['src'].to_parent(self.data['src'].c.center_x,self.data['src'].c.center_y)
			dst=self.data['dst'].to_parent(self.data['dst'].c.center_x,self.data['dst'].c.center_y)
			if src[0] < dst[0]:
				if src[1] < dst[1]:
					self.pos=src
					src=(0,0)
					self.size=(dst[0] - src[0],dst[1] - src[1])
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
			print("src="+str(src))
			print("dst="+str(dst))
			self.canvas.before.clear()
			with self.canvas.before:
				Color(0,0,0,1)
#				Line(points=[src,dst])
		return super().redraw(*args)
		
	def resolve(self,d=None):
		for i in App.get_running_app().panel.walk(restrict=True):
			if isinstance(i,SchemaObject):
				if d['uuid'].hex == i.data['uuid'].hex:
					return(i)
		return(None)
	
	def __init__(self,data=None,src=None,dst=None,dir=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)
		data['type']=type(self)
		if 'src' in data:
			if data['src'] is None:
				data['src']=src
			else:
				if type(data['src']) is dict:
					data['src']=self.resolve(data['src'])
		else:
			data['src']=src
		if 'dst' in data:
			if data['dst'] is None:
				data['dst']=dst
			else:
				if type(data['dst']) is dict:
					data['dst']=self.resolve(data['dst'])
		else:
			data['dst']=dst
		data['src'].wantlink.append(data['dst'])
		data['src'].wantlink[-1].e.append(self)
		data['dst'].wantlink.append(data['src'])
		data['dst'].wantlink[-1].e.append(self)
		self.direction=dir
		self.menuvisible=False
		Clock.schedule_once(self.redraw,0.05)