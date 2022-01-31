from kivymd.app import MDApp

from app.nodeeditor import NodeEditor
from app.mainpanel import MainPanel

class TestApp(MDApp):
	
	def load(self,*args):
		pass
		
	def save(self,*args):
		pass
		
	def newnode(self,*args):
		pass
		
	def clear(self,*args):
		pass
	
	def build(self):
		root=MainPanel(menu=[
			{
				'icon':'file-import',
				'callback':self.load
			},
			{
				'icon':'file-export',
				'callback':self.save
			},
			{
				'icon':'new-box',
				'callback':self.newnode
			},
			{
				'icon':'nuke',
				'callback':self.clear
			}
		])
		return root
		
TestApp().run()
		
		