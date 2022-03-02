from app.schemaobject import SchemaObject
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextField
from kivy.uix.textinput import TextInput
from kivymd.uix.filemanager import MDFileManager
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from widget.fieldtable import FieldTable,coldef
from widget.typelist import TypeList
from kivy.metrics import dp 

class NodeEditor(SchemaObject):
		
	iconpath=None

	def redraw(self,*args):
		super(NodeEditor,self).redraw(args)
#PAs tout compris
		self.s.height=self.size[1]-self.tb.size[1]-self.t.size[1]
		
	def on_size(self,*args):
		self.redraw(args)
			
	def addline(self,*args):
		self.dt.addline()
		
	def select_image(self,path):
		if self.icon:
			self.tb.remove_widget(self.icon)
		self.iconpath=path
		self.icon=Image(source=path)
		self.tb.add_widget(self.icon)
		self.exit_manager()
		
	def exit_manager(self,*args):
		self.manager_open=False
		self.file_manager.close()
		
	def addimage(self,*args):
		self.file_manager.show(App.get_running_app().apppath)
		self.manager_open=True
	
	def save(self,*args):
		data={
			'icon': self.iconpath,
			'fieldlist':self.dt.gettable(),
			'title':self.t.text
		}
		self.parent.remove_widget(self)
		for i in data['fieldlist']:
			for j in i:
				if j == '':
					Snackbar(text='Aaarg, all field definitions must be complete').open()
					return False
		self.cb(data)
		
	def cancel(self,*args):
		if self.parent:
			self.parent.remove_widget(self)
	
	def removeline(self,*args):
		for i in self.dt.children:
			if hasattr(i,'selected'):
				if i.selected:
					self.dt.remove_line(i)
		
	def __init__(self,data=None,cb=None,**kwargs):
		super(NodeEditor,self).__init__(data=data,**kwargs)
		self.tb=MDToolbar()
		self.tb.left_action_items=[["plus",lambda x: self.addline()],["minus",lambda x:self.removeline()],["file-image",lambda x: self.addimage()],["content-save",lambda x: self.save()],["step-backward",lambda x: self.cancel()]]
		self.tb.title="Node Editor"
		self.dt=FieldTable(coldata=[
			coldef(n='FieldName',c=TextInput),
			coldef(n='DisplayName',c=TextInput),
			coldef(n='FieldType',c=TypeList)
		],size_hint=(1,None),height=1000)
		self.dt.bind(minimum_height=self.dt.setter('height'))
		self.s=ScrollView(do_scroll_y=True,size_hint=(1,None),size=self.size)
		self.s.add_widget(self.dt)
		self.t=MDTextField(hint_text='Node Title',size_hint=(1,None))
		self.content=BoxLayout(orientation='vertical',padding=[0,0,0,0])
		self.content.add_widget(self.t)
		self.content.add_widget(self.s)
		self.content.add_widget(self.tb)
		self.add_widget(self.content)
		self.s.height=self.size[1]-self.s.size[1]-self.t.size[1]
		self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_image,
            preview=True,
        )
		self.manager_open=False
		self.icon=None
		self.cb=cb
		self.bind(size=self.redraw,pos=self.redraw)
		Clock.schedule_once(self.redraw,0.05)