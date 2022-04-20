from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.label import MDLabel

import commons

class Field(BoxLayout):
		
	def compute_size(self):
		if len(self.t.hint_text)>len(self.t.helper_text):
			x=self.t.hint_text
		else:
			x=self.t.helper_text
		z=MDLabel(text=x,size_hint=(None,None))
		z.text_size=(None,None)
		z.texture_update()
		w2=z.texture_size[0]*1.3
		self.t.width=w2
		return w2

	def __init__(self,labeltext,defaultvalue,**kwargs):
		super(Field,self).__init__(**kwargs)
		self.size_hint=(None,None)
		self.orientation='horizontal'
		self.t=MDTextField(hint_text=defaultvalue,size_hint=(1,None),multiline=False,helper_text=labeltext,helper_text_mode='persistent')
		self.add_widget(self.t)
		self.width=self.compute_size()