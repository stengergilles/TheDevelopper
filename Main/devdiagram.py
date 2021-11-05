import os.path
import json
import zipfile
from types import SimpleNamespace


class ObjectDescription(object):
    className = ""
    classAttributes = []
    classInheritancyParent = None
    classInheritancyChilds = []
    classOperations = []

class Operation(object):
    operationName = ""
    operationParameters = []
    operationReturns = []

class Signature(object):
    signatureName = ""
    signatureType = ""
    cardinality = ""

datamodel = []

def _GenerateData(topic=None, parent=None):
    newClass = ObjectDescription()
    newClass.className = topic.title
    if hasattr(topic, 'labels'):
        s=Signature()
        for i in topic.labels:
            if ":" in i:
                l=i.split(":")
                s.signatureName=l[0]
                s.signatureType=l[2]
                s.cardinality=l[1]
            else:
                s.signatureName=i
                s.signatureType=None
                s.cardinality=None
            newClass.classAttributes.append(s)
    newClass.classInheritancyParent = parent
    if hasattr(topic,'children'):
        if hasattr(topic.children,'attached'):
            for i in topic.children.attached:
                newClass.classInheritancyChilds.append(_GenerateData(topic=i,parent=newClass))
        if hasattr(topic.children,'detached'):
            for i in topic.children.detached:
                newClass.classInheritancyChilds.append(_GenerateData(topic=i,parent=newClass))
    return newClass

def _loadXmind(name=None):
    with zipfile.ZipFile(name) as f:
        if "content.json" in f.namelist():
            data = f.open("content.json").read().decode('utf-8')
    sh = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    for i in sh:
        if "Inheritancy" in i.title:
            datamodel.append(_GenerateData(topic=i.rootTopic))
    return datamodel

def loadDevDiagram(name=None):
    ret = None
    if os.path.splitext(name)[1] == ".xmind":
        ret = _loadXmind(name=name)
    return ret