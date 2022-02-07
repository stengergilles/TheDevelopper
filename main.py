from kivymd.app import MDApp 

from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel

from kivy.core.window import Window
from kivy.metrics import dp

import os

class TestApp(MDApp):
	
	apppath=os.path.dirname(os.path.realpath(__file__))
	
	def resize(self,*args):
		self.root.on_size(args)
	
	def load(self,*args):
		pass
		
	def save(self,*args):
		pass
		
	def newnode(self,*args):
		from app.nodeeditor import NodeEditor
		n=NodeEditor(data=None,cb=self.newnodecb)
		n.pinned=True
		self.root.add_widget(n)
		
	def newnodecb(self,data):
		from app.nodegraph import NodeGraph
		n=NodeGraph(data=data,pos=(dp(100),dp(100)),size_hint=(None,None))
		self.root.add_widget(n)
		
	def clear(self,*args):
		pass
	
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
		return self.root
		
TestApp().run()
		
		