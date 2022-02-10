from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel

class coldef:
	name=None
	classref=None
	height=None
	
	def __init__(self,n=None,c=None,f=None):
		self.name=n
		self.classref=c

class FieldTable(BoxLayout):
	
	def on_touch_down(self,touch):
		for i in self.children:
			if hasattr(i,'selected'):
				i.selected=False
			else:
				i.selected=False
			if i.collide_point(*touch.pos):
				i.selected=True
				return i.on_touch_down(touch)
		return False
			
	def __init__(self,coldata=None,**kwargs):
		super(FieldTable,self).__init__(**kwargs)
		self.orientation='vertical'
		self.coldata=coldata
		h=GridLayout(size_hint=(1,None))
		h.cols=len(coldata)
		for i in self.coldata:
			c=MDLabel(text=i.name,size_hint=(1,None))
			c.texture_update()
			c.height=c.texture.size[1]
			h.add_widget(c)
		self.add_widget(h)
		
	def addline(self):		
			l=GridLayout(size_hint=(1,None))
			l.cols=len(self.coldata)
			for i in self.coldata:
				w=i.classref(size_hint=(1,None))
				if hasattr(w,"text") and hasattr(w,"line_height"):
					w.text="X"
					w.height=w.line_height
					w.text=""
				if hasattr(w,"padding"):
					w.padding=[0,0,0,0]
				l.add_widget(w)
			self.add_widget(l)
	
	def gettable(self):
			ret=[]
			x=0
			y=0
			l=[]
			for i in self.walk(restrict=True):
				if hasattr(i,"text"):
					l.append(i.text)
					x = x + 1
					if x >= len(self.coldata):
						x=0
						y=y+1
						ret.append(l)
						l=[]
			return ret
			
	def remove_line(self,w):
		y=w.y
		for i in self.children:
			if i.y == y:
				self.remove_widget(i)