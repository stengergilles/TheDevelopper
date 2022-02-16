from app.schemaobject import SchemaObject
from app.schemaobject import schema
from json import dump

def save(path=None):
	try:
		with open(path,'w') as fp:
			dump(schema,fp)
			fp.close()
			return(True)
	except Exception as e:
		print(e)
		return(False)