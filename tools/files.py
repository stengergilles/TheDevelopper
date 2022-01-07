import json
import jsonpickle

def isjson(f=None):
	try:
		ret=json.load(open(f,'r'))
		return ret
	except:
		return None

def save(fname=None, root=None,tosave=None):
	with open(fname,'w') as file:
		for i in root.children:
			if type(i) is tosave:
			    file.write(jsonpickle.encode(i))

def load(fname=None,root=None,toload=None):
	with open(fname,'r') as file:
		zz=jsonpickle.decode(file.read())
		root.add_widget(zz)