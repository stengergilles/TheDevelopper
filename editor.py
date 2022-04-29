from kivy.extras.highlight import PythonLexer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
import commons

class Editor(BoxLayout):
	
	def getlinecount(self):
		return self.c.text.count('\n')
		
	def getline(self,l):
		return self.c.text.split('\n')[l]
		
	def getlines(self):
		return self.c.text.split('\n')
	
	def on_parent(self,instance,value):
		if self.parent:
			self.c.background_color=commons.mainpanel.theme_background_color()
			self.c.foreground_color=commons.mainpanel.theme_primary_color()

	def __init__(self,**kwargs):
		super(Editor,self).__init__(**kwargs)
		self.c=CodeInput(lexer=PythonLexer())
		self.orientation='horizontal'
		self.size_hint=(None,None)
		self.add_widget(self.c)