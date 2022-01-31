from kivymd.uix.circularlayout import MDCircularLayout
from kivymd.uix.button import MDFloatingActionButton
from kivy.metrics import dp

class Menu(MDCircularLayout):
	data=None
		
	def __init__(self,data=None,**kwargs):
		super(Menu,self).__init__(**kwargs)
		self.data=data
		self.degree_spacing=30
		self.size_hint=(None,None)
		self.size=(dp(64),dp(64))
		for i in data:
			m=MDFloatingActionButton(icon=i['icon'],size_hint=(None,None),size=(dp(8),dp(8)))
			m.bind(on_press=i['callback'])
			self.add_widget(m)
			
			