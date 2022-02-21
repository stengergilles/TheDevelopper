from enum import Enum
from app.schemaobject import SchemaObject

class direction(Enum):
	SRCDST=1
	DSTSRC=2
	BOTH=3
	NONE=4
	
class SchemaEdge(SchemaObject):
	
	def __init__(self,data=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)