class ObjectDescription(object):
	className=""
	classAttributes=[]
	classInheritancyParent=None
	classInheritancyChilds=[]
	classOperations=[]
	
class Operation(object):
	operationName=""
	operationParameters=[]
	operationReturns=[]
	
class Signature(object):
	signatureName=""
	signatureType=""
	
import os.path
from types import SimpleNamespace
import zipfile
import json

datamodel=[]

def _GenerateData(topic=None,parent=None):
    newClass=ObjectDescription()
    newClass.className=topic.title
	if hasattr(topic,'labels'):
	   pass    
    newClass.classInheritancyParent=parent
    

def _loadXmind(name=None):
	with zipfile.ZipFile(name) as f:
		if "content.json" in f.namelist():
			data=f.open("content.json").read().decode('utf-8')
	sh=json.loads(data,object_hook=lambda d: SimpleNamespace(**d))
	for i in sh:
		if "Inheritancy" in i.title:
			_GenerateData(topic=i.rootTopic)

def loadDevDiagram(name=None):
	ret=None
	if os.path.splitext(name)[1] == ".xmind":
		ret=_loadXmind(name=name)
	return ret