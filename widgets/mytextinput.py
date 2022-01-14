from kivy.uix.textinput import TextInput

class MyTextInput(TextInput):

	def __init__(self,**kwargs):
		super(MyTextInput,self).__init__(**kwargs)

	def on_touch_down(self, touch):
		
		return super().on_touch_down(touch)
