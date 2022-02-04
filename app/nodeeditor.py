from app.schemaobject import SchemaObject
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.label import MDLabel
from kivymd.uix.filemanager import MDFileManager
from kivy.app import App
from kivy.uix.image import Image

class coldef:
	name=None
	classref=None
	height=None
	
	def __init__(self,n=None,c=None,f=None):
		self.name=n
		self.classref=c

class FieldTable(BoxLayout):
	
	def __init__(self,coldata=None,**kwargs):
		super(FieldTable,self).__init__(**kwargs)
		self.orientation='vertical'
		self.coldata=coldata
		h=GridLayout(size_hint=(1,None))
		h.cols=len(coldata)
		for i in self.coldata:
			c=MDLabel(text=i.name,text_size=(None,None))
			c.texture_update()
			c.size=c.texture.size
			h.add_widget(c)
		self.add_widget(h)
		
	def addline(self):		
			l=GridLayout(size_hint=(1,None))
			l.cols=len(self.coldata)
			for i in self.coldata:
				w=i.classref(size_hint=(1,None))
				l.add_widget(w)
			self.add_widget(l)
			
	def gettable(self):
			ret=[]
			x=0
			y=0
			l=[]
			for i in self.children:
				if not type(i) is MDLabel:
					l.append(i.text)
					x =x + 1
					if x > len(self.coldata):
						x=0
						y=y+1
						ret.append(l)
						l=[]
			return ret
			
class NodeEditor(SchemaObject):
		
	iconpath=None
		
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
			'fieldlist':self.dt.gettable()
		}
		self.parent.remove_widget(self)
		self.cb(data)
		
	def cancel(self,*args):
		if self.parent:
			self.parent.remove_widget(self)
		
	def __init__(self,data=None,cb=None,**kwargs):
		super(NodeEditor,self).__init__(data=data,**kwargs)
		self.tb=MDToolbar()
		self.tb.left_action_items=[["plus",lambda x: self.addline()],["file-image",lambda x: self.addimage()],["content-save",lambda x: self.save()],["step-backward",lambda x: self.cancel()]]
		self.tb.title="Node Editor"
		self.dt=FieldTable(coldata=[
			coldef(n='FieldName',c=MDTextFieldRect),
			coldef(n='DisplayName',c=MDTextFieldRect),
			coldef(n='FieldType',c=MDTextFieldRect)
		],size_hint=(1,None),height=1000)
		self.dt.bind(minimum_height=self.dt.setter('height'))
		self.s=ScrollView(do_scroll_y=True,size=self.size)
		self.s.add_widget(self.dt)
		self.content=BoxLayout(orientation='vertical')
		self.content.add_widget(self.s)
		self.content.add_widget(self.tb)
		self.add_widget(self.content)
		self.s.size=(self.s.size[0]-self.tb.size[0],self.s.size[1]-self.s.size[1])
		self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_image,
            preview=True,
        )
		self.manager_open=False
		self.icon=None
		self.cb=cb