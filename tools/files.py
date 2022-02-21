import jsonpickle

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
		
def loadschema(path=None):
	try:
		with open(path,'r') as fp:
			app.settings.schema=jsonpickle.decode(fp.read())
			return(True)
	except Exception as e:
		print(e)
		return(False)