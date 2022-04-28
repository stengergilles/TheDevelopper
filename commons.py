import json
import importlib
from pydoc import locate
from kivy.metrics import dp
from kivy.clock import Clock
import traceback
import os

def init():
	global start_dir
	global schema
	global mainpanel
	global program_path
	global icon_path
	start_dir=None
	schema=[]
	mainpanel=None
	Clock.max_iteration=1500
	program_path = os.path.dirname(os.path.realpath(__file__))
	icon_path=os.path.join(program_path,'icons')
	
def filesave(filename=None):
	text="["
	for i in schema:
		s=i.serialize()
		print(str(s))
		s['type']=str(type(i))
		text=text+json.dumps(s)+","
	text=(text+"]").replace(",]","]")
	try:
		with open(filename,'w') as file:
			file.write(text)
			file.close()
			return None,True
	except Exception as e:
		return str(e),False
		
def resolvtype(t=None):
	return locate(t.replace("<class '","").replace("'>",""))
	
def resolvnode(id):
	for i in schema:
		if i.id==id:
			return i
	return None
		
def fileload(filename=None):
	try:
		with open(filename,'r') as file:
			myschema=json.load(file)
			grnode=locate('graphnode.GraphNode')
			group=locate('groupnode.GroupNode')
			label=locate('graphlabel.GraphLabel')
#load nodes
			for i in myschema:
				classtype=resolvtype(i['type'])
				if classtype is label:
					size=(dp(i['size'][0]),dp(i['size'][1]))
					pos=(dp(i['pos'][0]),dp(i['pos'][1]))
					w=classtype(
						pos=pos,
						size=size,
						title=i['title'],
						size_hint=(None,None),
						id=i['id'],
						body=i['text']
					)		
					mainpanel.add_widget(w)
				if classtype is grnode:
					size=(dp(i['size'][0]),dp(i['size'][1]))
					pos=(dp(i['pos'][0]),dp(i['pos'][1]))
					w=classtype(
						pos=pos,
						size=size,
						title=i['title'],
						size_hint=(None,None),
						id=i['id'],
						fields=i['fields']
					)		
					mainpanel.add_widget(w)
#resolv links
			for i in myschema:
				classtype=resolvtype(i['type'])
				if classtype is grnode:
					for j in i['links']:
						ltype=resolvtype(j['linkclass'])
						n=resolvnode(i['id'])
						ll=ltype(
							j['src'],
							j['dst'],
							j['kind']
						)
						n.links.append(ll)
#resolv groups
			for i in myschema:
				classtype=resolvtype(i['type'])
				if classtype is group:
					g=group(
						id=i['id'],
						title=i['title'],
						size_hint=(None,None),
						pos=(dp(i['pos'][0]),dp(i['pos'][1])),
						size=(dp(i['size'][0]),dp(i['size'][1]))
					)
					for j in i['members']:
						m=mainpanel.get_node_by_id(j)
						m.parent.remove_widget(m)
						g._content.add_widget(m)
					mainpanel.add_widget(g)
				
	except Exception as e:
		print(traceback.format_exc())
		return str(e),False	
	return None,True