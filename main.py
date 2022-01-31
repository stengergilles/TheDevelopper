from kivymd.app import MDApp

from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel

class TestApp(MDApp):
	
	def load(self,*args):
		print("Load")
		
	def save(self,*args):
		pass
		
	def newnode(self,*args):
		pass
		
	def clear(self,*args):
		pass
	
	def build(self):
		root=MainPanel(menu=[
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
		return root
		
TestApp().run()
		
		