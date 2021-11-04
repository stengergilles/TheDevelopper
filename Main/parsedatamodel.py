import json
import argparse
import os.path
import os
import logging
import zipfile
from types import SimpleNamespace
import pathlib

topicpath=[]
typelist=("none","int","float","long","bool","complex","str","unicode","list","tuple","xrange","dict","set")

def whichFile(query=None,base=None):
    ret=[]
    for root,dirs,files in os.walk(base):
        for file in files:
            if pathlib.Path(os.path.join(root,file)).suffix == ".py":
               with open(os.path.join(root,file)) as f:
                    if query in f.read():
                       ret.append(f.name)
                       f.close()
    return ret

def whichFileByName(f=None,base=None):
    for root,dirs,files in os.walk(base):
        for file in files:
            if file == f:
                return(root)

def getcurrentpath(sep=None):
    return sep.join(topicpath)

def getparentpath():
    return topicpath[0:-1]

def generatedata(dest=None,topic=None,forceparent=None):
    topicpath.append(topic.title)
    parentpath=getparentpath()
    if (len(parentpath)>=1):
        parent=parentpath[-1]
    else:
        parent='object'
    if forceparent:
       parent=forceparent
    ppath=".".join(parentpath).lower()
    print(getcurrentpath(sep="."))
    fields=""
    constructor=""
    imports=""
    if hasattr(topic,'labels'):
        for i in topic.labels:
            if ":" in i:
                s=i.split(":")
                typename=s[2]
                cardinality=s[1]
                fieldname=s[0]
                if cardinality == "1n":
                    fields += "    " + fieldname + ": []\n"
                    typename='list'
                else:
                    fields += "    " + fieldname + ":" + typename + "\n"
            else:
                fields += "    " + i + ": None\n"
                fieldname=i
                typename='none'
            constructor += "        self."+fieldname+"=kwargs.get('"+fieldname+"')\n"
            found=False
            for t in typelist:
                if t == typename:
                    found=True
            if not found:
                imports += "from ## import " + typename + "\n"
    if hasattr(topic,'children'):
        dirpath=getcurrentpath("/").lower()
        os.makedirs(dest + "/" + dirpath)
        f=open(dest+"/"+dirpath+"/__init__.py","w+")
        if parent != 'object':
            f.write('from '+ppath+" import "+parent+"\n")
        if len(imports):
            f.write(imports)
        f.write("class "+topic.title+"("+parent+"):\n")
        if len(fields):
            f.write(fields)
        f.write("    def __init__(self,*args,**kwargs):\n")
        if parent != 'object':
            f.write("        super("+topic.title+",self).__init__(*args,**kwargs)\n")
        if len(constructor):
            f.write(constructor)
        if not parent and not len(constructor):
            f.write("        pass\n")
        f.close()
        for i in topic.children.attached:
            generatedata(dest=dest,topic=i) 
        if hasattr(topic.children,'detached'):
            for i in topic.children.detached:
                generatedata(dest=dest,topic=i,forceparent='object')
    else:
        dirpath="/".join(parentpath).lower()
        f=open(dest+"/"+dirpath+"/"+topic.title+".py","w+")
        if parent != 'object':
           f.write('from '+ppath+" import "+parent+"\n")
        if len(imports):
            f.write(imports)
        f.write("class "+topic.title+"("+parent+"):\n")
        if len(fields):
            f.write(fields)
        f.write("    def __init__(self,*args,**kwargs):\n")
        if parent != 'object':
            f.write("        super("+topic.title+",self).__init__(*args,**kwargs)\n")
        if len(constructor):
            f.write(constructor)
        if parent=='object' and not len(constructor):
            f.write("        pass\n")
        f.close()
    topicpath.pop()

def getobject(f=None):
    ret=[]
    dummy=open(f)
    for l in dummy.readlines():
        if l.startswith("from ##"):
            ret.append(l.split(' ')[3].rstrip('\n'))
    dummy.close()
    return ret

def resolvimport(base=None):
    for name in whichFile(query="from ##",base=base):
        f=open(name,"r") 
        for oname in getobject(f.name):
            dirname=whichFileByName(f=oname+'.py',base=base)
            if dirname:
                dirname=dirname.replace(base+'/','').replace('/','.') + '.' + oname
            else:
                zz=whichFile(query="class "+oname,base=base)
                if not len(zz):
                   raise Exception("Fatal Error:" + oname + " class not found in Model")
                if len(zz[0]) == 0:
                   raise Exception("Fatal Error: import for object " + oname + "Not Found")
                dirname=zz[0].replace(base+'/','').replace('/__init__.py','').replace('/','.')
            s=f.read().replace("from ## import "+oname,"from "+dirname+" import "+oname)
            f.close()
            g=open(f.name,"w")
            g.write(s)
            g.close()
            f=open(name,"r")
            dirname=""

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-m","--map",dest="map",help="The map to parse",required=True)
    parser.add_argument("-d","--destination",dest="dest",help="The destination",required=True)
    args=parser.parse_args()
    if not os.path.isdir(args.dest):
        os.makedirs(args.dest)
    with zipfile.ZipFile(args.map) as f:
        if "content.json" in f.namelist():
            data=f.open("content.json").read().decode('utf-8')
    sh=json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    args.dest=args.dest.rstrip("/")
    for i in sh:
        if "Inheritancy" in i.title:
            print(i.title)
            generatedata(dest=args.dest,topic=i.rootTopic)
    resolvimport(base=args.dest)
