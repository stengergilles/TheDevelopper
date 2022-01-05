import json
import os
import jsonpickle
from pprint import pprint

def isjson(f=None):
	try:
		ret=json.load(os.open(f))
		return ret
	except:
		return None

def save(fname=None, root=None,tosave=None):
	with open(fname,'w') as file:
		for i in root.children:
			if type(i) is tosave:
			    print('writing:')
			    pprint(i.__getstate__())
			    file.write(jsonpickle.encode(i))