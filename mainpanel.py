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
from trash import Trash
from form import Form
from field import Field

from editor import Editor

import os

import commons

class MainPanel(FloatLayout):
	
	def get_real_parent(self):
		return self
	
	def get_node_by_id(self,id):
		for i in self.walk(restrict=True):
			if hasattr(i,'id'):
				if i.id==id:
					return i
		return None
		
	def get_node_target_link(self,node):
		ret=[]
		for i in self.walk(restrict=True):
			if hasattr(i,'links'):
				for j in i.links:
					if j.dst is node:
						ret.append(i)
		return ret
	
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
			v=self.d.content_cls.nodetitle.text
			w=GraphNode(size=(dp(100),dp(100)),size_hint=(None,None),pos=self.m.pos)
			w.title=v
			for i in self.d.content_cls.members.walk(restrict=True):
				if type(i) is MDTextField:
					w._form.add_field(name=i.text,value="",default="")
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
			self.d.content_cls.data=self
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
			if type(i) is GraphNode or type(i) is Editor:
				i.parent.remove_widget(i)
				i=None
		for i in self.walk(restrict=True):
			if type(i) is GroupNode:
				i.parent.remove_widget(i)
				i=None
		
	def center_and_fit(self,x,y,w,h):		
# compute bounds
		minx=-1
		maxx=0
		miny=-1
		maxy=0
		for i in self.walk(restrict=True):
			if not type(i) is Editor:
				if i.x >maxx:
					maxx=i.x
				if i.x <minx:
					minx=x
				else:
					if minx==-1:
						minx=i.x
				if i.y > maxy:
					maxy=i.y
				if i.y<miny:
					miny=i.y
				else:
					if miny==-1:
						miny=i.y
		minw=maxx-minx
		minh=maxy-miny
		tw=w/minw
		th=h/minh
		for i in self.walk(restrict=True):
			if isinstance(i,GraphNode) or isinstance(i,GroupNode):
				i.pos=(x+i.x*tw,y+i.y*th)
				if i.top>self.height:
					i.translatetop=(i.top-self.height)
					i.y=i.y-i.translatetop
				else:
					i.translatetop=0
				if i.right>self.width:
					i.translateright=i.right-self.width
					i.x=i.x-i.translateright
				else:
					i.translateright=0
				i.factor=(tw,th)
				i.base=(x,y)
				if isinstance(i,GroupNode):
					i._trigger()
								
	def code_graph(self):
		self.editor.x=0.05*self.width
		self.editor.y=0.05*self.height
		self.editor.size=(self.width*0.9,self.height*0.5)
		self.add_widget(self.editor)
		self.center_and_fit(0.05*self.width,self.height*0.55,self.width*0.9,self.height*0.45)
		self.editoractive=True
	
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
			if not i is self and isinstance(i,RelativeLayout) and not isinstance(i.parent.parent.parent,GroupNode) and not isinstance(i,Trash) or isinstance(i,Form) or isinstance(i,Field):
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
			if self.editoractive==True:
				self.remove_widget(self.editor)
				self.editoractive=False
				for i in self.walk(restrict=True):
					if hasattr(i,'factor'):
						x=(i.pos[0]-i.base[0]+i.translateright)/i.factor[0]
						y=(i.pos[1]-i.base[1]+i.translatetop)/i.factor[1]
						i.pos=(x,y)
						delattr(i,'factor')
						delattr(i,'base')
						delattr(i,'translatetop')
						delattr(i,'translateright')
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
		},{
			'icon':'book-edit',
			'name':'Editor',
			'callback':self.code_graph
		}
		])
		self.menuvisible=False
		self.havemodal=False
		self.add_widget(Trash(pos_hint={'right':1,'bottom':1},size_hint=(None,None)))
		self.editor=Editor()
		self.editoractive=False