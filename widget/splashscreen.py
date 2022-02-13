from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen

class SplashScreen(Screen):
	def __init__(self,img=None,**kwargs):
		super(SplashScreen,self).__init__(**kwargs)
		f=FloatLayout()
		f.add_widget(AsyncImage(source=img))
		self.add_widget(f)
	