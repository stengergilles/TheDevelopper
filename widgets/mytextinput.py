from kivy.uix.textinput import TextInput

class MyTextInput(TextInput):

	def __getstate__(self):
		return {"text": self.text}

	def __init__(self,**kwargs):
		super(MyTextInput,self).__init__(**kwargs)