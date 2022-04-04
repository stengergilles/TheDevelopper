from kivymd.uix.circularlayout import MDCircularLayout
from kivymd.uix.button import MDFloatingActionButton
from kivy.metrics import dp
from functools import partial
from kivy.app import App
from kivy.graphics import Ellipse,Color

class Menu(MDCircularLayout):
	data=None

	def buttonpress(self,*args,**kwargs):
		if kwargs['n'] is None:
			pass
		else:
			kwargs['n']['callback']()
		self.parent.dismiss_menu()
		
	def __init__(self,data=None,**kwargs):
		super(Menu,self).__init__(**kwargs)
		self.visible=False
		self.data=data
		self.degree_spacing=50
		self.size_hint=(None,None)
		self.size=(dp(200),dp(200))
		for i in data:
			m=MDFloatingActionButton(icon=i['icon'],size_hint=(None,None),size=(dp(8),dp(8)))
			m.bind(on_press=partial(self.buttonpress,n=i))
			self.add_widget(m)
		