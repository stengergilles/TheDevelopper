from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class DataObject(object):
	displayname=None

	def __init__(self):
		self.displayname={}

	def addField(self,name=None,displayname=None):
		self.displayname[name]=displayname

	def getLayout(self): 
		ret=GridLayout(size_hint=(None,1))
		ret.cols=2
		w=0
		h=0
		for i in self.displayname.keys():
			l=Label(text=self.displayname[i],size_hint_y=None,size_hint_x=None,font_size='12sp')
			l.texture_update()
			l.size=(l.texture_size[0]*1.2,l.texture_size[1]*2)
			ret.add_widget(l)
			t=TextInput(multiline=False,size_hint_y=None,size_hint_x=None,font_size='12sp')
			texture=t._create_line_label("xxxxxxxxxx")
			ret.add_widget(t)
			if l.texture_size[1]+texture.size[0]>w:
				w=l.texture_size[1]+texture.size[0]
			t.size=(texture.size[0]*1.4,l.texture_size[1]*1.8)
			h += l.texture_size[1]
		ret.size=(w*1.20,h)
		return ret