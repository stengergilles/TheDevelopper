from kivymd.uix.label import MDIcon
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
import commons

class Trash(RelativeLayout):
	
	def __init__(self,**kwargs):
		super(Trash,self).__init__(**kwargs)
		self.t=MDIcon(theme_text_color="Custom",text_color=commons.mainpanel.theme_primary_color(),icon='trash-can',size_hint=(None,None),pos=(0,0),size=(dp(48),dp(48)))
		self.add_widget(self.t)