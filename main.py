from kivymd.app import MDApp 

from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel
from app.nodegraph import NodeGraph
from app.schemaobject import SchemaObject
from tools.files import save
from widget.file import FileDialog

from kivy.core.window import Window
from kivy.metrics import dp

import os
import sys
import kivy
from enum import Enum

class Mode(Enum):
	SAVE=1
	LOAD=1
	
class TestApp(MDApp):
	
	apppath=os.path.dirname(os.path.realpath(__file__))
	currentfile=None

	def select_file(self,path):
		if self.mode == Mode.SAVE:
			save(self.root,path)
		else:
			pass
		self.fm.fileexitmgr()
		self.remove_widget(self.fm)
		
	def resize(self,*args):
		self.root.on_size(args)
	
	def load(self,*args):
		self.fm.mode=Mode.LOAD
		self.add_widget(self.fm)
		
	def save(self,*args):
		self.fm.mode=Mode.SAVE
		self.add_widget(self.fm)
		
	def newnode(self,*args):
		n=NodeEditor(data=None,cb=self.newnodecb)
		n.pinned=True
		self.root.add_widget(n)
		
	def newnodecb(self,data):
		n=NodeGraph(data=data,pos=(dp(100),dp(100)),size_hint=(None,None))
		self.root.add_widget(n)
		
	def clear(self,*args):
		for i in self.root.walk(restrict=True):
			if isinstance(i,SchemaObject):
				i.parent.remove_widget(i)
	
	def build(self):
		self.root=MainPanel(menu=[
			{
				'name':'file-load',
				'icon':'file-import',
				'callback':self.load
			},
			{
				'name':'file-save',
				'icon':'file-export',
				'callback':self.save
			},
			{
				'name':'new-node',
				'icon':'new-box',
				'callback':self.newnode
			},
			{
				'name':'clear-graph',
				'icon':'nuke',
				'callback':self.clear
			}
		])
		self.theme_cls.theme_style="Light"
		Window.bind(size=self.resize)
		self.fm=FileDialog(mode=Mode.SAVE,exitmgr=self.select_file)
		return self.root
	
if kivy.__version__ != '2.0.0':
	print('Bad kivy version ' + kivy.__version__ + ' 2.0.0 required')
	sys.exit(1)

TestApp().run()
		
		