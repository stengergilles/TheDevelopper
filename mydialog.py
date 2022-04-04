from kivy.uix.boxlayout import BoxLayout

class MyDialog(BoxLayout):
	
	def __init__(self,**kwargs):
		super(MyDialog,self).__init__(**kwargs)
		self.orientation="vertical"
		self.size_hint=(1,None)
		
	def getvaluebytype(self,t=None,f=None):
		for i in self.walk(restrict=True):
			if hasattr(i,f) and type(i) is t:
				return getattr(i,f)
		return None
		
	def getrefbytype(self,t=None,f=None):
		for i in self.walk(restrict=True):
			if hasattr(i,f) and type(i) is t:
				return i
		return None