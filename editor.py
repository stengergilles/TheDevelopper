from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.label import MDLabel
from kivy.extras.highlight import PythonLexer
from kivy.metrics import dp

class Editor(BoxLayout):
	
	def on_parent(self,instance,value):
		if self.parent:
			self.c.background_color=self.parent.theme_background_color()
			self.c.foreground_color==self.parent.theme_primary_color()

	def __init__(self,**kwargs):
		super(Editor,self).__init__(**kwargs)
		self.c=CodeInput(lexer=PythonLexer())
		self.orientation='horizontal'
		self.size_hint=(None,None)
		self.add_widget(self.c)