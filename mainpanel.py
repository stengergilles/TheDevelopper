from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from menu import Menu
from nodeeditor import EditNodeDialog
from graphnode import GraphNode
from groupnode import GroupNode
from filedialog import FileSaveDialog
from filedialog import FileLoadDialog

import os

import commons

class MainPanel(FloatLayout):
	
	def get_node_by_id(self,id):
		for i in self.walk(restrict=True):
			if hasattr(i,'id'):
				if i.id==id:
					return i
		return None
	
	def dismiss_menu(self):
		if hasattr(self,'m'):
			self.remove_widget(self.m)
			self.menuvisible=False
	
	def dismiss(self):
		if hasattr(self,'d'):
			self.havemodal=False
			self.d.dismiss(force=True)
			self.remove_widget(self.d)
			
	def get_panel_canvas(self):
		return self.canvas
	
	def new_node(self,*args):
		if args:
			v=self.d.content_cls.getvaluebytype(t=MDTextField,f='text')
			w=GraphNode(size=(dp(100),dp(100)),size_hint=(None,None),pos=self.m.pos)
			w.title=v
			self.add_widget(w)
			self.dismiss()
		else:
			self.havemodal=True
			self.d=MDDialog(
				title='New Node',
				type='custom',
				content_cls=EditNodeDialog(),
				buttons=[
					MDFlatButton(text='Cancel',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.dismiss()),
					MDFlatButton(text='Ok',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.new_node('back'))
				],
				pos_hint={'center_x':0.5,'center_y':0.5},
				auto_dismiss=False
			)
			self.add_widget(self.d)
		
	def load_graph(self,*args):
		if args:
			self.d.content_cls.exit_manager()
			self.nuke_graph()
			filename=self.d.content_cls.d.current_path
			if os.path.isfile(filename):
				msg,status=commons.fileload(filename)
				if status:
					msg="File successfully loaded"
				else:
					msg="Error loading file:"+msg
				Snackbar(text=msg).open()
				self.dismiss()
		else:
			self.d=MDDialog(
				title='File Load',
				type='custom',
				content_cls=FileLoadDialog(),
				buttons=[
					MDFlatButton(text='Cancel',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.dismiss()),
					MDFlatButton(text='Ok',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.load_graph('back'))
				],
				pos_hint={'center_x':0.5,'center_y':0.5},
				auto_dismiss=False
			)
			self.add_widget(self.d)
		
	def save_graph(self,*args):
		if args:
			self.d.content_cls.exit_manager()
			filename=self.d.content_cls.f.text
			if filename != "":
				msg,status=commons.filesave(filename)
				if status:
					msg="File successfully saved"
				else:
					msg="Error saving file:"+msg
				Snackbar(text=msg).open()
				self.dismiss()
		else:
			self.d=MDDialog(
				title='File Save',
				type='custom',
				content_cls=FileSaveDialog(),
				buttons=[
					MDFlatButton(text='Cancel',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.dismiss()),
					MDFlatButton(text='Ok',theme_text_color='Custom',text_color=self.theme_primary_color(),on_press=lambda *x: self.save_graph('back'))
				],
				pos_hint={'center_x':0.5,'center_y':0.5},
				auto_dismiss=False
			)
			self.add_widget(self.d)
		
	def nuke_graph(self):
		for i in self.walk(restrict=True):
			if type(i) is GraphNode:
				i.parent.remove_widget(i)
				i=None
		for i in self.walk(restrict=True):
			if type(i) is GroupNode:
				i.parent.remove_widget(i)
				i=None
		self.canvas.clear()
	
	def text_color(self):
		x=self.app.theme_cls.text_color
		return x
	
	def bg_color(self):
		x=self.app.theme_cls.bg_normal
		return Color(x[0],x[1],x[2],x[3])
		
	def primary_color(self):
		x=self.app.theme_cls.primary_color
		return Color(x[0],x[1],x[2],x[3])
		
	def primary_color_light(self):
		x=self.app.theme_cls.primary_light
		return Color(x[0],x[1],x[2],x[3])
		
	def theme_primary_color(self):
		return self.app.theme_cls.primary_color
		
	def have_children_touch(self,touch,excl=None):
		if hasattr(self,'d'):
			if self.havemodal and self.d.collide_point(*touch.pos):
				return self.d
		if hasattr(self,'m'):
			if self.menuvisible and self.m.collide_point(*touch.pos):
				return self.m
		for i in self.walk(restrict=True):
			if not i is self and i.collide_point(*touch.pos):
				if not i is excl:
					return i
		return None
		
	def translate_childs(self,dx=None,dy=None):
		for i in self.walk(restrict=True):
			if not i is self and isinstance(i,RelativeLayout) and not isinstance(i.parent.parent.parent,GroupNode):
				i.pos=(i.pos[0]+dx,i.pos[1]+dy)

	def show_menu(self,m=None,x=None,y=None,data=None):
		self.m=m
		self.m.center_x=x
		self.m.center_y=y
		self.m.data=data
		self.menuvisible=True
		self.add_widget(self.m)
			
	def on_touch_down(self,*args):
		if self.have_children_touch(*args):
			return super(MainPanel,self).on_touch_down(*args)
		else:
			touch=args[0]
			if not touch.is_double_tap:
				self.moving=True
				return True
			else:
				if self.menuvisible:
					self.dismiss_menu()
				else:
					self.show_menu(m=self.panelmenu,x=touch.x,y=touch.y)
				return True
		
	def on_touch_move(self,*args):
		if self.moving:
			touch=args[0]
			self.translate_childs(dx=touch.dx,dy=touch.dy)
			return(True)
		else:
			return super(MainPanel,self).on_touch_move(*args)
	
	def on_touch_up(self,*args):
		if self.have_children_touch(*args):
			return super(MainPanel,self).on_touch_up(*args)
		else:
			if self.moving:
				self.moving=False
				return True
		return False
		
	def __init__(self,app=None,**kwargs):
		super(MainPanel,self).__init__(**kwargs)
		self.app=app
		self.moving=False
		commons.mainpanel=self
		self.panelmenu=Menu(data=[{
			'icon':'new-box',
			'name':'New',
			'callback':self.new_node
		},{
			'icon':'file-import',
			'name':'Load',
			'callback':self.load_graph
		},
		{
			'icon':'file-export',
			'name':'Save',
			'callback':self.save_graph
		},{
			'icon':'nuke',
			'name':'Nuke',
			'callback':self.nuke_graph
		}
		])
		self.menuvisible=False
		self.havemodal=False