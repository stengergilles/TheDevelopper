from enum import IntEnum
from form import Form
from groupeditor import EditGroupDialog
from groupnode import GroupNode
from groupnode import ProxyStackLayout
from kivy.clock import Clock
from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.graphics import Triangle
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon
from kivymd.uix.textfield import MDTextField
from math import sqrt
from menu import Menu
from nodeeditor import EditNodeDialog
from trash import Trash
from uuid import uuid4

import commons

class linkKind(IntEnum):
	SRCDST=1
	DSTSRC=2
	BOTH=3
	NONE=4

class Link:
	src=None
	dst=None
	kind=None
	line=None
	triangle=None
	triangle2=None
	color=None
	
	def __init__(self,src,dst,kind):
		if type(src) is str:
			self.src=commons.resolvnode(src)
		else:
			self.src=src
		if type(dst) is str:
			self.dst=commons.resolvnode(dst)
		else:
			self.dst=dst
		self.kind=kind

class GraphNode(RelativeLayout):
	
	title=StringProperty("")
	links=ListProperty([])
	id=StringProperty("")
	
	def serialize(self):
		ret={}
		ret['id']=self.id
		ret['title']=self.title
		ret['links']=[]
		if not hasattr(self,'factor'):
			ret['pos']=(self.pos[0]/dp(1),self.pos[1]/dp(1))
		else:
			x=(self.pos[0]-self.base[0]+self.translateright)/self.factor[0]
			y=(self.pos[1]-self.base[1]+self.translatetop)/self.factor[1]
			ret['pos']=(x/dp(1),y/dp(1))
		ret['size']=(self.size[0]/dp(1),self.size[1]/dp(1))
		for i in self.links:
			ret['links'].append({
				'src':str(i.src.id),
				'dst':str(i.dst.id),
				'kind':int(i.kind),
				'linkclass':str(Link)
			})
		ret['fields']=self._form.serialize()
		return ret	
	
	def dismiss(self):
		s=self.parent.parent.parent.parent
		if not hasattr(s,'d'):
			s=self.parent
		s.havemodal=False
		s.d.dismiss(force=True)
		s.remove_widget(s.d)
	
	def new_group(self,*args):
		if args:
			v=self.parent.d.content_cls.nodetitle.text
			g=GroupNode(title=v,size=(dp(100),dp(100)),size_hint=(None,None),pos=(self.parent.width/2,self.parent.height/2))
			self.parent.add_widget(g)
			self.parent.remove_widget(self.parent.m.data)
			g._content.add_widget(self.parent.m.data)
			self.parent.remove_widget(self)
			g._content.add_widget(self)
			self.dismiss()
		else:
			self.parent.havemodal=True
			self.parent.d=MDDialog(
				title='New Group',
				type='custom',
				content_cls=EditGroupDialog(),
				buttons=[
					MDFlatButton(text='Cancel',theme_text_color='Custom',text_color=self.parent.theme_primary_color(),on_press=lambda *x: self.dismiss()),
					MDFlatButton(text='Ok',theme_text_color='Custom',text_color=self.parent.theme_primary_color(),on_press=lambda *x: self.new_group('back'))
				],
				pos_hint={'center_x':0.5,'center_y':0.5},
				auto_dismiss=False
			)
			self.parent.add_widget(self.parent.d)
		return True
	
	def on_links(self,instance,value):
		self._trigger()
	
	def link_srcdst(self):
		self.links.append(Link(src=self,dst=self.parent.m.data,kind=linkKind.SRCDST))
		return True
	
	def link_dstsrc(self):
		self.links.append(Link(src=self.parent.m.data,dst=self,kind=linkKind.DSTSRC))
		return True
		
	def link_both(self):
		self.links.append(Link(src=self,dst=self.parent.m.data,kind=linkKind.BOTH))
		return True
		
	def link_none(self):
		self.links.append(Link(src=self,dst=self.parent.m.data,kind=linkKind.NONE))
		return True
		
	def layout(self,*args):
		if self.parent:
			self._title.color=self.parent.theme_primary_color()
			self._icon.color=self._title.color
		self._title.texture_update()
		self.handle_w=max(dp(32),self._title.texture_size[1])
		self.handle_h=self.handle_w
		self.size=(self.handle_w+self._title.texture_size[0],self.handle_h)
		self._title.text_size=(self._title.texture_size[0],self.handle_h)
		self._title.texture_update()
		self._title.size=self._title.texture_size
		self._title.pos=(self.handle_w,0)
		self._icon.size=(self.handle_w,self.handle_h)
		self._icon.pos=(0,0)
		
	def on_title(self,instance,value):
		self._title.text=value
		self._trigger()
		return True

	def in_handle(self,touch):
		i=self.to_widget(*touch.pos)
		if 0<i[0]<self.handle_w:
			if 0<i[1]<self.handle_h:
				return True
		return False
	
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			if self.in_handle(touch):
				self.moving=True
				return True
			else:			
				if self._title.collide_point(*self.to_widget(*touch.pos)):
					self.edit_title()
					return True
				return False
		else:
			return False
		
	def on_touch_move(self,touch):
		if self.moving:
			if hasattr(self,'_form'):
				if not self.isingroup() and self._form.count:
					p=touch.pos
					dx=p[0]-self.x
					dy=p[1]-self.y
					self._form.pos=(self._form.x+dx,self._form.y+dy)		
			self.pos=touch.pos
			return True
		else:
			return False
	
	def on_touch_up(self,touch):
		if self.moving:
			self.moving=False
			self._trigger()
			tgt=self.parent.have_children_touch(touch,excl=self)
			if isinstance(tgt,GraphNode) and not tgt is self:
				self.parent.show_menu(m=self.nodemenu,x=touch.pos[0],y=touch.pos[1],data=tgt)
				return False
			if isinstance(tgt,GroupNode):
				self.parent.remove_widget(self)
				tgt._content.add_widget(self)
				return True
			if isinstance(tgt,Trash):
				self.parent.remove_widget(self)
				return True
		else:
			return False
			
	def on_parent(self,instance,p):
		if p is None:
			commons.mainpanel.remove_widget(self._form)
			if self.flinecolor:
				commons.mainpanel.canvas.remove(self.flinecolor)
			if self.fline:
				commons.mainpanel.canvas.remove(self.fline)
			for j in self.links:
				if j.src is self:
					if j.line:
						commons.mainpanel.canvas.remove(j.line)
					if j.triangle:
						commons.mainpanel.canvas.remove(j.triangle)
					if j.triangle2:
						commons.mainpanel.canvas.remove(j.triangle2)
					if j.color:
						commons.mainpanel.canvas.remove(j.color)
			for i in commons.mainpanel.get_node_target_link(self):
					for j in i.links:
						if self is j.dst:
							if j.line:
								commons.mainpanel.canvas.remove(j.line)
							if j.triangle:
								commons.mainpanel.canvas.remove(j.triangle)
							if j.triangle2:
								commons.mainpanel.canvas.remove(j.triangle2)
							if j.color:
								commons.mainpanel.canvas.remove(j.color)
							i.links.remove(j)						
			commons.schema.remove(self)
		else:
			if not self in commons.schema:
				commons.schema.append(self)
				if type(p) is ProxyStackLayout:
					commons.mainpanel.remove_widget(self._form)
					if self.flinecolor:
						commons.mainpanel.canvas.remove(self.flinecolor)
					if self.fline:
						commons.mainpanel.canvas.remove(self.fline)
					self.fline=None
					self.flinecolor=None
				if p is commons.mainpanel:
					self._form.pos=(self.x+dp(60),self.y+dp(100))
					p.add_widget(self._form)
		if isinstance(p,ProxyStackLayout):
			p.layout(instance)
		return True
			
	def drawArrow(self,p=None,dx=None,dy=None):
		n=sqrt(dx*dx+dy*dy)
		if not n:
			return None
		dx=dx*dp(15)/n
		dy=dy*dp(15)/n		
		cos=0.866
		sin=0.5
		end1=(p[0]+dx*cos+dy*-sin,p[1]+dx*sin+dy*cos)
		end2=(p[0]+dx*cos+dy*sin,p[1]+dx*-sin+dy*cos)
		return Triangle(points=(p[0],p[1],end1[0],end1[1],end2[0],end2[1]))
		
	def isingroup(self):
		if type(self.parent) is ProxyStackLayout:
			return True
		return False
		
	def draw(self,*args):
		if self.canvas and self.parent:
			self.layout()
			pc=self.parent.get_panel_canvas()
			self.canvas.before.remove(self.parent.bg_color())
			if self.main_background:
				self.canvas.before.remove(self.main_background)
			self.main_background=Rectangle(pos=(0,0),size=self.size)
			self.canvas.before.add(self.parent.bg_color())
			self.canvas.before.add(self.main_background)
			if self.moving:
				if self.handle_color:
					self.canvas.before.remove(self.handle_color)
				self.handle_color=self.parent.primary_color_light()
				self.canvas.before.add(self.handle_color)
				if self.handle:
					self.canvas.before.remove(self.handle)
				self.handle=Rectangle(pos=(0,0),size=(self.handle_w,self.handle_h))
				self.canvas.before.add(self.handle)
			for i in self.links:
				if i.color:
					pc.remove(i.color)
				i.color=self.parent.primary_color_light()
				pc.add(i.color)
				if i.line:
					pc.remove(i.line)
				src=(i.src.pos[0]+self._icon.size[0]/2,i.src.pos[1]+self._icon.size[1]/2)
				if i.src.isingroup():
					src=i.src.parent.parent.parent.to_parent(*src)
				dst=(i.dst.pos[0]+self._icon.size[0]/2,i.dst.pos[1]+self._icon.size[1]/2)
				if i.dst.isingroup():
					dst=i.dst.parent.parent.parent.to_parent(*dst)
				i.line=Line(points=[src[0],src[1],dst[0],dst[1]])
				pc.add(i.line)
				if i.triangle:
					pc.remove(i.triangle)
				if i.triangle2:
					pc.remove(i.triangle2)
				if i.kind==linkKind.SRCDST:
					i.triangle=self.drawArrow(p=dst,dx=-(dst[0]-src[0]),dy=-(dst[1]-src[1]))
				if i.kind==linkKind.DSTSRC:
					i.triangle=self.drawArrow(p=src,dx=(dst[0]-src[0]),dy=(dst[1]-src[1]))
				if i.kind==linkKind.BOTH:
					i.triangle=self.drawArrow(p=dst,dx=-(dst[0]-src[0]),dy=-(dst[1]-src[1]))
					i.triangle2=self.drawArrow(p=src,dx=(dst[0]-src[0]),dy=(dst[1]-src[1]))
				if i.triangle:
					pc.add(i.triangle)
				if i.triangle2:
					pc.add(i.triangle2)
			if not self.isingroup() and self._form.count:
				if self.flinecolor:
					pc.remove(self.flinecolor)
				self.flinecolor=self.parent.primary_color_light()
				pc.add(self.flinecolor)
				if self.fline:
					pc.remove(self.fline)
				zz=self.to_parent(self._icon.size[0]/2,self._icon.size[1]/2)
				self.fline=Line(points=[zz[0],zz[1],self._form.pos[0],self._form.pos[1]])
				pc.add(self.fline)
		return False
									
	def on_size(self,*args):
		self._trigger()
		return False
		
	def on_pos(self,instance,p):	
		self._trigger()
		if self.parent:
			for i in self.parent.walk(restrict=True):
				if isinstance(i,GraphNode) and not i is self:
					i._trigger()
		return False
		
	def edit_title(self,*args):
		p=self.parent.get_real_parent()
		if args:
			v=p.d.content_cls.nodetitle.text
			for i in p.d.content_cls.members.walk(restrict=True):
				if type(i) is MDTextField:
					f=self._form.find_field(i.text)
					if f is None:
						self._form.add_field(name=i.text)
			if v!= "":
				self.title=v
			p.dismiss()
		else:
			p.havemodal=True
			p.d=MDDialog(
				title='Edit Node',
				type='custom',
				content_cls=EditNodeDialog(),
				buttons=[
					MDFlatButton(text='Cancel',theme_text_color='Custom',text_color=self.parent.theme_primary_color(),on_press=lambda *x: self.dismiss()),
					MDFlatButton(text='Ok',theme_text_color='Custom',text_color=self.parent.theme_primary_color(),on_press=lambda *x: self.edit_title('back'))
				],
				pos_hint={'center_x':0.5,'center_y':0.5},
				auto_dismiss=False
			)
			p.d.content_cls.nodetitle.hint_text=self._title.text
			p.d.content_cls.nodedata=self
			p.add_widget(p.d)	
		
	def __init__(self,title='Untitled Node',id=None,fields=None,**kwargs):
		self._trigger=Clock.create_trigger(self.draw)
		super(GraphNode,self).__init__(**kwargs)
		if not id:
			self.id=str(uuid4())
		else:
			self.id=id
		self.moving=False
		self.handle=None
		self.main_background=None
		self.handle_color=None
		self.fline=None
		self.flinecolor=None
		self._form=Form()
		self._form.pos=(self.x+dp(60),self.y+dp(100))
		if fields:
			for i in fields:
				for k in i:
					self._form.add_field(name=k,value=i[k],default="")
		commons.mainpanel.add_widget(self._form)
		self._title=Label(text=self.title,size_hint=(None,None),max_lines=1,text_size=(None,None),valign='middle')
		self._icon=MDIcon(theme_text_color="Custom",text_color=commons.mainpanel.theme_primary_color(),icon='circle',pos=(0,0),font_size=self._title.font_size,padding=(0,0))
		self.add_widget(self._title)
		self.add_widget(self._icon)
		self.title=title
		self.nodemenu=Menu(data=[{
			'icon':'arrow-right',
			'name':'srcdst',
			'callback':self.link_srcdst
		},{
			'icon':'arrow-left',
			'name':'dstsrc',
			'callback':self.link_dstsrc
		},{
			'icon':'arrow-all',
			'name':'both',
			'callback':self.link_both
		},{
			'icon':'chart-line',
			'name':'none',
			'callback':self.link_none
		},{
			'icon':'group',
			'name':'group',
			'callback':self.new_group
		}])
		commons.schema.append(self)
