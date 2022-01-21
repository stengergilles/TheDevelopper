from kivy.effects.scroll import ScrollEffect

class MyScrollEffect(ScrollEffect):
	
	def __init__(self,**kwargs):
		super(MyScrollEffect,self).__init__(**kwargs)
		
	def on_scroll(self,*args):
		print("on scroll")
		super(MyScrollEffect,self).on_scroll(*args)