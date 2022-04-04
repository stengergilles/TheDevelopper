from kivymd.uix.textfield import MDTextField
from mydialog import MyDialog

class EditGroupDialog(MyDialog):
	
	def __init__(self,**kwargs):
		super(EditGroupDialog,self).__init__(**kwargs)
		self.nodetitle=MDTextField(hint_text='Group Title')
		self.add_widget(self.nodetitle)