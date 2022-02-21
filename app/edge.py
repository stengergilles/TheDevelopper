from enum import Enum
from app.schemaobject import SchemaObject
from kivy.graphics import Line,Color

class direction(Enum):
	SRCDST=1
	DSTSRC=2
	BOTH=3
	NONE=4
	
class SchemaEdge(SchemaObject):

	def redraw(self, *args):
		if self.data['src'] and self.data['dst']:
			with self.canvas.before:
				Color(1,1,1,1)
				Line(self.data['src'].pos,self.data['dst'].pos)
		return super().redraw(*args)
	
	def __init__(self,data=None,src=None,dst=None,dir=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)
		data['type']=type(self)
		data['src']=src
		data['dst']=dst
		self.direction=dir