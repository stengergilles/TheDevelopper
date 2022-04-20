from kivy.uix.codeinput import CodeInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.label import MDLabel
from kivy.extras.highlight import PythonLexer
from kivy.metrics import dp
#warning. dependance applicative
import commons

class Editor(BoxLayout):
	
	def add_bounded_label(self,text):
		ret=MDLabel(text=text,size_hint=(None,None),text_size=(0,0),halign='right')
		ret.texture_update()
		ret.size=ret.text_size=ret.texture.size
		return ret
	
	def show_lines(self):
		self.l.clear_widgets()
		self.l.total_size=0
		for i in range(self.lstart,self.lstart+10):
			l=self.add_bounded_label(text=str(i))
			self.l.total_size=self.l.total_size+l.height
			self.l.add_widget(l)
	
	def __init__(self,**kwargs):
		super(Editor,self).__init__(**kwargs)
		self.l=BoxLayout(orientation='vertical',size_hint=(0.2,None))
		self.lstart=1
		self.add_widget(self.l)
		self.c=CodeInput(lexer=PythonLexer())
		self.orientation='horizontal'
		self.size_hint=(None,None)
		self.add_widget(self.c)
		self.show_lines()