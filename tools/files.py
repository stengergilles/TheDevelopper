import json
import os
import jsonpickle

def isjson(f=None):
	try:
		ret=json.load(os.open(f))
		return ret
	except:
		return None

def save(fname=None, root=None):
	with open(fname,'w') as file:
		file.write(jsonpickle.encode(root))