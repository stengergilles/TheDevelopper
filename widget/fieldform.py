from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox

class FieldForm(BoxLayout):
	
	def update_field(self,*args):
		if type(args[0]) is MDTextField:
			self.data[args[0].f]=args[0].text
		if type(args[0]) is MDCheckbox:
			self.data[args[0].f]=args[1]
		
	def __init__(self,fielddef=None,data=None,**kwargs):
		super(FieldForm,self).__init__(**kwargs)
		self.orientation='vertical'
		self.rows=len(fielddef)-1
		s = 1 if len(fielddef) == 1 else 1/(len(fielddef)-1)
		self.fielddef=fielddef
		self.data=data
		total=0
		for idx,val in enumerate(fielddef):
			if idx >=1:
				if val[2] == '' or val[2] == 'String' or val[2] == 'Integer' or val[2] == 'Float':
					t=MDTextField(helper_text=val[1],size_hint=(None,None),width=self.size[0])
					t.multiline=False
					t.helper_text_mode='persistent'
					t.text="X"
					t.height=t.minimum_height
					t.text=""
					t.f=val[0]
					t.bind(on_text_validate=self.update_field)
					if t.f in self.data:
						t.text=self.data[t.f]
					else:
						self.data[t.f]=t.text
					self.add_widget(t)
					t.text=""
					total=total+t.height
					if val[2] == 'Integer':
						t.input_filter='int'
					if val[2] == 'Float':
						t.input_filter='float'
				else:
					if val[2] == 'Boolean':
						g=GridLayout(size_hint=(None,None),width=self.size[0])
						g.cols=2
						l=MDLabel(text=val[1],size_hint=(1,None))
						l.texture_update()
						l.height=l.texture.size[1]
						l.shorten=True
						c=MDCheckbox(size_hint=(1,None))
						c.height=l.texture.size[1]
						c.f=val[0]
						if c.f in self.data:
							c.active=self.data[c.f]
						else:
							c.active=False
						c.bind(active=self.update_field)
						g.add_widget(c)
						g.add_widget(l)
						g.height=c.height
						self.add_widget(g)	
						total=total + c.height	
		self.height=total
				