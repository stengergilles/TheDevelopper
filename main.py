from kivymd.app import MDApp 
from kivymd.uix.snackbar import Snackbar
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
	
class TheDevelopper(MDApp):
	
	apppath=os.path.dirname(os.path.realpath(__file__))
	currentfile=None

	def select_file(self,path):
		if self.mode == Mode.SAVE:
			if save(path):
				Snackbar(text='File successfully Saved').open()
		else:
			pass
		self.fm.fileexitmgr()
		self.panel.remove_widget(self.fm)
		
	def resize(self,*args):
		self.panel.on_size(args)
	
	def load(self,*args):
		self.mode=Mode.LOAD
		self.panel.add_widget(self.fm)
		
	def save(self,*args):
		self.mode=Mode.SAVE
		self.panel.add_widget(self.fm)

	def newnode(self,*args):
		n=NodeEditor(data=None,cb=self.newnodecb)
		n.pinned=True
		self.panel.add_widget(n)
		
	def newnodecb(self,data):
		n=NodeGraph(data=data,pos=(dp(100),dp(100)),size_hint=(None,None))
		self.panel.add_widget(n)
		
	def clear(self,*args):
		for i in self.panel.walk(restrict=True):
			if isinstance(i,SchemaObject):
				i.parent.remove_widget(i)

	def makepanel(self):
		self.panel=MainPanel(menu=[
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
		self.fm=FileDialog(mode=Mode.SAVE,exitmgr=self.select_file,apppath=self.apppath)
		return (self.panel)
		
	def build(self):
		return(self.makepanel())
	
if kivy.__version__ != '2.0.0':
	print('Bad kivy version ' + kivy.__version__ + ' 2.0.0 required')
	sys.exit(1)

if __name__ == '__main__':
	TheDevelopper().run()
	