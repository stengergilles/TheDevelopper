from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel

class FieldForm(GridLayout):
	
	def __init__(self,fielddef=None,**kwargs):
		super(FieldForm,self).__init__(**kwargs)
		self.cols=1
		self.rows=len(fielddef)-1
		s = 1 if  len(fielddef) == 1 else 1/(len(fielddef)-1)
		self.fielddef=fielddef
		for idx,val in enumerate(fielddef):
			if idx >=1:
				g=GridLayout(cols=2,rows=1,size_hint=(1,s))
				g.add_widget(MDLabel(text=val[1],size_hint=(1,s),font_style='Caption',shorten=True,valign='top'))
				g.add_widget(MDLabel(text='toto',size_hint=(1,s),valign='top',font_style='Caption'))
				self.add_widget(g)
		print(self.size)
				