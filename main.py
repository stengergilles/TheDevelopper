from kivymd.app import MDApp 
from kivymd.uix.snackbar import Snackbar
from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel
from app.nodegraph import NodeGraph
from app.schemaobject import SchemaObject
from tools.files import saveschema
from tools.files import loadschema
from widget.file import FileDialog
from kivy.core.window import Window
from kivy.metrics import dp

import os
import sys
import kivy
from enum import Enum

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

import app.settings 

class Mode(Enum):
	SAVE=1
	LOAD=2
	
class TheDevelopper(MDApp):
	
	apppath=os.path.dirname(os.path.realpath(__file__))
	currentfile=None

	def select_file(self,path):
		self.currentfile=path
		if self.mode == Mode.SAVE:
			if saveschema(path):
				Snackbar(text='File successfully Saved').open()
			else:
				Snackbar(text='Error Saving File').open()
		if self.mode == Mode.LOAD:
			self.clear()
			if loadschema(path):
				self.schematowidget()
				Snackbar(text='File successfully Loaded').open()
			else:
				Snackbar(text='Error loading file')
		self.fm.fileexitmgr()
		self.panel.remove_widget(self.fm)
		self.fm=None
		
	def load(self,*args):
		self.mode=Mode.LOAD
		self.fm=FileDialog(mode=Mode.LOAD,exitmgr=self.select_file,apppath=self.apppath)
		self.panel.add_widget(self.fm)
		
	def save(self,*args):
		self.mode=Mode.SAVE
		self.fm=self.fm=FileDialog(mode=Mode.SAVE,exitmgr=self.select_file,apppath=self.apppath)
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
		app.settings.schema=[]
		
	def schematowidget(self):
		for i in app.settings.schema:
			if i:
				p=(dp(i['pos'][0]),dp(i['pos'][1]))
				s=(dp(i['size'][0]),dp(i['size'][1]))
				z=i['type'](data=i,pos=p,size_hint=(None,None))
				self.panel.add_widget(z)

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
		self.theme_cls.primary_palette="Blue"
		return (self.panel)
		
	def build(self):
		return(self.makepanel())
	
app.settings.init()

if __name__ == '__main__':
	TheDevelopper().run()
	