from json import dump
from json import load

import app.settings

def saveschema(path=None):
	try:
		with open(path,'w') as fp:
			dump(app.settings.schema,fp)
			fp.close()
			return(True)
	except Exception as e:
		print(e)
		return(False)
		
def loadschema(path=None):
	try:
		with open(path,'r') as fp:
			app.settings.schema=load(fp)
			return(True)
	except Exception as e:
		print(e)
		return(False)