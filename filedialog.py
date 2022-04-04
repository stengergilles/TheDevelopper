from mydialog import MyDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp

import commons

import os.path

class FileSaveDialog(MyDialog):
	
	def open(self,*args):
		pass
		
	def dismiss(self,*args):
		pass

	def exit_manager(self,*args):
		if self.f.text != "" and self.d.current_path not in self.f.text:
			self.f.text=os.path.join(self.d.current_path,self.f.text)
		if self.f.text != self.d.current_path and self.f.text:
			self.d.close()	
		
	def select_path(self,*args):
		if len(args):
			path=args[0]
			if os.path.isfile(path):
				self.f.text=path
				for i in self.parent.parent.parent.buttons:
					if i.text=="Ok":
						i.dispatch('on_press')
		
	def __init__(self,**kwargs):
		super(FileSaveDialog,self).__init__(**kwargs)
		self.size=(dp(800),dp(600))
		self.d=MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path,size_hint=(1,1))
		self.d._window_manager=self
		self.add_widget(self.d)
		self.d.show(commons.start_dir)
		self.f=MDTextField(hint_text='File to Save',size_hint=(1,None))
		self.add_widget(self.f)
		
class FileLoadDialog(MyDialog):
	
	def open(self,*args):
		pass
		
	def dismiss(self,*args):
		pass
		
	def exit_manager(self,*args):
		self.d.close()
		
	def select_path(self,*args):
		if len(args):
			if os.path.isfile(args[0]):
				self.d.current_path=args[0]
				for i in self.parent.parent.parent.buttons:
					if i.text=="Ok":
						i.dispatch('on_press')
		
	def __init__(self,**kwargs):
		super(FileLoadDialog,self).__init__(**kwargs)
		self.size=(dp(800),dp(600))
		self.d=MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path,size_hint=(1,1))
		self.auto_dismiss=True
		self.d._window_manager=self
		self.add_widget(self.d)
		self.d.show(commons.start_dir)