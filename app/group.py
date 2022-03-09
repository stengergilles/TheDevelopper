from app.schemaobject import SchemaObject

class SchemaGroup(SchemaObject):
	
	def __init__(self,data=None,**kwargs):
		super(SchemaGroup,self).__init__(data=data,**kwargs)