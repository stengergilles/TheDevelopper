from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckBox

class FieldForm(BoxLayout):
	
	def __init__(self,fielddef=None,**kwargs):
		super(FieldForm,self).__init__(**kwargs)
		self.orientation='vertical'
		self.rows=len(fielddef)-1
		s = 1 if  len(fielddef) == 1 else 1/(len(fielddef)-1)
		self.fielddef=fielddef
		total=0
		for idx,val in enumerate(fielddef):
			if idx >=1:
				print(val[2])
				if val[2] == '' or val[2] == 'String' or val[2] == 'Integer' or val[2] == 'Float':
					t=MDTextField(helper_text=val[1],size_hint=(None,None),width=self.size[0])
					t.multiline=False
					t.helper_text_mode='persistent'
					t.text="X"
					t.height=t.minimum_height
					self.add_widget(t)
					t.text=""
					total=total+t.height
					if val[2] == 'Integer':
						t.input_filter='int'
					if val[2] == 'Float':
						t.input_filter='float'
				else:
					if val[2] == 'Boolean':
						g=Gridlayout(size_hint=(None,None),width=self.size[0])
		self.height=total
				