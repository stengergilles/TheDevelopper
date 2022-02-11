from tkinter.filedialog import SaveAs
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel

from enum import Enum

class Mode(Enum):
	SAVE=1
	LOAD=2

class FileDialog(BoxLayout):

	def fileexitmgr(self,*args):
		self.manager_open=False
		self.file_manager.close()
		self.mode=None

	def __init__(self,mode=None,exitmgr=None,**kwargs):
		super(FileDialog,self).__init__(**kwargs)
		self.mode=mode
		self.exitmgr=exitmgr
		self.manager_open=False
		self.file_manager = MDFileManager(exit_manager=self.fileexitmgr,select_path=self.exitmgr,preview=True)
		if self.mode==mode.SAVEAS:
			self.filename=MDLabel(hint_text="New File")
		else:
			self.filename=None
		self.add(self.file_manager)
		if self.filename:
			self.add(self.filename)
