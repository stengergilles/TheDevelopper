from kivy.uix.floatlayout import FloatLayout
from pprint import pprint

class MyFloatLayout(FloatLayout):
	
	def __getstate__(self):
		state=self.__dict__.copy()
		pprint(state)
		return state
		
	def __setstate__(self,state):
		pass
		
	def __init__(self,**kwargs):
		super(MyFloatLayout,self).__init__(**kwargs)