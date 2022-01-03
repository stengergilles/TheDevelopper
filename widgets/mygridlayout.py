from kivy.uix.gridlayout import GridLayout

class MyGridLayout(GridLayout):
	
	def __getstate__(self):
		return {"cols":2}
		
	def __setstate__(self,state):
		pass
		
	def __init__(self,**kwargs):
		super(MyGridLayout,self).__init__(**kwargs)