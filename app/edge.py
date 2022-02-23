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
			self.parent.canvas.before.clear()
			with self.parent.canvas.before:
				Color(0,0,0,1)
				src=self.data['src'].to_parent(self.data['src'].c.center_x,self.data['src'].c.center_y)
				dst=self.data['dst'].to_parent(self.data['dst'].c.center_x,self.data['dst'].c.center_y)
				Line(points=[src,dst])
		return super().redraw(*args)
		
	def resolve(self,d=None):
		print('d='+str(d))
		for i in App.get_running_app().panel.children.walk(restrict=True):
			if d['uuid'] == i.data['uuid'].hex:
				return(i)
		return(None)
	
	def __init__(self,data=None,src=None,dst=None,dir=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)
		data['type']=type(self)
		if data['src'] is None:
			data['src']=src
		else:
			if type(data['src']) is dict:
				data['src']=self.resolve(data['src'])
		if data['dst'] is None:
			data['dst']=dst
		else:
			if type(data['dst']) is dict:
				data['dst']=self.resolve(data['dst'])
		self.direction=dir
		self.menuvisible=False
		Clock.schedule_once(self.redraw,0.05)