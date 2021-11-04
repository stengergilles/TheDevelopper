import json
import argparse
import os.path
import os
import logging
import zipfile
from types import SimpleNamespace
import pathlib
import random
import string
import jsonpickle
import re

typelist=("none","int","float","long","bool","complex","str","unicode","list","tuple","xrange","dict","set")

class myparam:
    pass

class operation:
    name:str
    objectcontext:str
    parameters:[]
    returndata:[]

oplist=[]
importlist=[]

def whichFileByName(f=None,base=None):
    for root,dirs,files in os.walk(base):
        for file in files:
            if file == f:
                return(os.path.join(root,file).replace(base,'').lstrip("/"))

def findModuleClass(n=None,base=None):
    for root,dirs,files in os.walk(base):
        for file in files:
            if pathlib.Path(os.path.join(root,file)).suffix == ".py":
               with open(os.path.join(root,file)) as f:
                    if "class " + n in f.read():
                       return(root.replace(base,'').lstrip("/"))
 

def resolvimport(n=None, data=None):
    typeimport=None
    r=whichFileByName(f=n+".py",base=data)
    if not r:
       r=findModuleClass(n=n,base=data)
    if r:
       r=r.replace("/"+n+".py","")
       typeimport=(r.replace("/","."), n)
    return typeimport

def parsesig(topic=None,data=None):
    ret=[]
    for i in topic:
       p=None
       for j in i.title.split(':'):
           try:
              (importpath,objectname)=resolvimport(n=j,data=data)
              importlist.append((importpath,objectname))
              p=myparam()
              p.name="p_"+j+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
              p.type=objectname
           except Exception as e:
              if j in typelist:
                 p=myparam()
                 p.name=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
                 p.type=j
       if not p is None:
          ret.append(p)
    return(ret)
    
def makeoperation(dest=None,topic=None,data=None):
    objectname=None
    try:
        (importpath,objectname)=resolvimport(n=topic.title,data=data)
    except Exception as e:
        pass
    if not objectname is None:
        ret=[]
        for o in topic.children.attached:
            ret.append(makeoperation(dest=dest,topic=o,data=data))
            ret[-1].objectcontext=importpath+"."+objectname
        return ret 
    else:
        op=operation()
        op.name=topic.title
        op.objectcontext=None
        op.parameters=[]
        op.parameters.extend(parsesig(data=data,topic=[x for x in topic.children.attached if x.title == "parameters"][0].children.attached))
        op.returndata=[]
        op.returndata.extend(parsesig(data=data,topic=[x for x in topic.children.attached if x.title == "return"][0].children.attached))
        return(op)

def generatefunction(o:None,data:None):
    if o is None:
       return
    if o.objectcontext is None:
       s="def "
       s += o.name + "("
       for i in o.parameters:
           s+=i.name+"=None,"
       s+=")\n"
       s+="    Implementation."+o.name+"("
       for i in o.parameters:
           s+=i.name+","
       s+=")\n"
       s=s.replace(",)",")")
       return(s)
    else:
       objectname=o.objectcontext.split('.')[-1]
       objectpath=".".join(o.objectcontext.split('.')[0:-1])
       funcimport = "import Implementation."+objectpath
       pypath=data + "/" + "/".join(o.objectcontext.split('.')[0:-1])
       if os.path.exists(pypath + "/" + objectname + ".py"):
           pypath=pypath+"/"+objectname+".py"
       else:
           pypath=pypath + "/__init__.py"
       f=open(pypath,"r")
       data=f.read()
       data=re.sub(funcimport,"",data,re.MULTILINE)
       funcimport += "\n"
       data=re.sub("^class (.*):$",
            funcimport +
            "class \g<1>:\n    "+o.name+"=Implementation."+objectpath+"."+o.name,
            data,
            flags=re.MULTILINE
       )
       f.close()
       f=open(pypath,"w")
       f.write(data)
       f.close()

def generateoperations(dest=None,topic=None,data=None):
    if topic.title=="Operations":
        if hasattr(topic,'children'):
            for i in topic.children.detached:
                o=makeoperation(dest=dest,topic=i,data=data)
                if type(o) is operation:
                   oplist.append(o)
                else:
                   oplist.extend(o)
            f=open(dest+"/__init__.py","w+")
            for i in set(importlist):
                f.write("from "+i[0]+" import " + i[1]+"\n")
            f.write("import Implementation\n\n")
            for i in set(importlist):
                f.write("def Create"+i[1]+"(*args,**kwargs):\n")
                f.write("    ret=" + i[1]+ "()\n")
                f.write("    for key,value in kwargs.iteritems():\n")
                f.write("        if hasattr(ret,key):\n")
                f.write("            setattr(ret,key,value)\n")
                f.write("        else:\n")
                f.write("            raise Exception('attribute '+key+' not found in object "+i[1]+"')\n\n")
                f.write("def Del"+i[1]+"(p=None):\n")
                f.write("    if type(p) is " + i[1]+":\n")
                f.write("        del p\n")
                f.write("    else:\n")
                f.write("        raise Exception('Object '+str(p)+' is of type '+type(p)+' expected "+i[1]+"')\n\n")
            f.write("\n")
            for o in oplist:
                s=generatefunction(o=o,data=data)
                if s:
                   f.write(s)
                   f.write("\n")
            f.close()
                
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-m","--map",dest="map",help="The map to parse",required=True)
    parser.add_argument("-d","--destination",dest="dest",help="The destination",required=True)
    parser.add_argument("-M","--datamodel",dest="datamodel",required=True)
    args=parser.parse_args()
    if not os.path.isdir(args.datamodel):
        raise(Exception("Model does not exist or is not readable"))
    if not os.path.isdir(args.dest):
        os.makedirs(args.dest)
    with zipfile.ZipFile(args.map) as f:
        if "content.json" in f.namelist():
            data=f.open("content.json").read().decode('utf-8')
    sh=json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    for i in sh:
        if i.title == "Operations":
            generateoperations(dest=args.dest,topic=i.rootTopic,data=args.datamodel)
