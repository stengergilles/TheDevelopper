import json
import jsonpickle

from app.schemaobject import SchemaObject

def isjson(f=None):
	try:
		ret=json.load(open(f,'r'))
		return ret
	except:
		return None

def save(fname=None, root=None,tosave=None):
	with open(fname,'w') as file:
		l=[]
		for i in root.children:
			if type(i) is tosave:
				l.append(i._getstate())
		file.write(jsonpickle.encode(l))

def load(fname=None,root=None,toload=None):
	with open(fname,'r') as file:
		zz=jsonpickle.decode(file.read())
		for i in zz:
			root.add_widget(toload(i))