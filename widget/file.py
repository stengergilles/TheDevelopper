
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField
import os

class FileDialog(BoxLayout):
	
	def on_size(self,*args):
		pass

	def open(self,*args):
		pass
		
	def select_path(self,path):
		if self.filename:
			if os.path.isdir(path):
				self.exitmgr(os.path.join(path,self.filename.text))
			else:
				self.exitmgr(path)

	def fileexitmgr(self,*args):
		self.manager_open=False
		self.file_manager.close()
		self.mode=None
			
	def dismiss(self,*args):
		pass

	def __init__(self,mode=None,exitmgr=None,apppath=None,**kwargs):
		super(FileDialog,self).__init__(**kwargs)
		self.orientation='vertical'
		self.mode=mode
		self.exitmgr=exitmgr
		self.manager_open=False
		self.file_manager = MDFileManager(exit_manager=self.fileexitmgr,select_path=self.select_path,preview=True)
		self.file_manager._window_manager=self
		if self.mode==mode.SAVE:
			self.filename=MDTextField(hint_text="New File")
		else:
			self.filename=None
		self.add_widget(self.file_manager)
		if self.filename:
			self.add_widget(self.filename)
		self.file_manager.show(apppath)