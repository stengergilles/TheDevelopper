import jsonpickle
import uuid

import app.settings

def saveschema(path=None):
	try:
		with open(path,'w') as fp:
			fp.write(jsonpickle.encode(app.settings.schema))
			fp.close()
			return(True)
	except Exception as e:
		print(e)
		return(False)	
		
def resolve(id=None):
		for i in app.settings.schema:
			if i['uuid'] == uuid.UUID(id):
				return i
		return None
		
def haveref(id=None):
	print(id)
	for i in app.settings.schema:
		for k,v in i.items():
			print(str(k))
			print(str(v))
			if str(v) == id:
				return(i,k)
	return None
	
def loadschema(path=None):
	try:
		with open(path,'r') as fp:
			app.settings.schema=jsonpickle.decode(fp.read())
			r=[]
			for i in app.settings.toresolv:
				if hasattr(i,'toresolve'):
					r.append(resolve(i.toresolve))
					app.settings.toresolv.remove(i)
			for i in r:
				z=haveref(i)
				print('after')
				if z:
					z[0][z[1]]=i
					print(z)
			return(True)
	except Exception as e:
		print(e)
		return(False)