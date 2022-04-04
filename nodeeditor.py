from kivymd.uix.textfield import MDTextField
from mydialog import MyDialog

class EditNodeDialog(MyDialog):
	
	def __init__(self,**kwargs):
		super(EditNodeDialog,self).__init__(**kwargs)
		self.nodetitle=MDTextField(hint_text='Node Title')
		self.add_widget(self.nodetitle)