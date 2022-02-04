from kivymd.app import MDApp 

from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel

from kivy.core.window import Window

import os

class TestApp(MDApp):
	
	apppath=os.path.dirname(os.path.realpath(__file__))
	
	def load(self,*args):
		pass
		
	def save(self,*args):
		pass
		
	def newnode(self,*args):
		from app.nodeeditor import NodeEditor
		data=[]
		n=NodeEditor(data=data,cb=self.newnodecb)
		n.pinned=True
		self.root.add_widget(n)
		
	def newnodecb(self,data):
		print('coucou')
		print('data='+str(data))
		
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
		return self.root
		
TestApp().run()
		
		