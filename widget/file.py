from tkinter.filedialog import SaveAs
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField

from enum import Enum

class Mode(Enum):
	SAVE=1
	LOAD=2

class FileDialog(BoxLayout):

	def fileexitmgr(self,*args):
		self.manager_open=False
		self.file_manager.close()
		self.mode=None

	def __init__(self,mode=None,exitmgr=None,apppath=None,**kwargs):
		super(FileDialog,self).__init__(**kwargs)
		self.orientation='vertical'
		self.mode=mode
		self.exitmgr=exitmgr
		self.manager_open=False
		self.file_manager = MDFileManager(exit_manager=self.fileexitmgr,select_path=self.exitmgr,preview=True)
		if self.mode==mode.SAVE:
			self.filename=MDTextField(hint_text="New File")
		else:
			self.filename=None
#		self.add_widget(self.file_manager)
		if self.filename:
			self.add_widget(self.filename)
		self.file_manager.show(apppath)