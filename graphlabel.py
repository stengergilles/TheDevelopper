from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.graphics import Rectangle,Color,Line,Triangle
from kivymd.uix.label import MDIcon,MDLabel

class GraphLabel(RelativeLayout):
	
	title=StringProperty("")
	body=StringProperty("")
	
	def draw(self):
		self.canvas.before.add(Color(0,0,0,0.2))
		self.canvas.before.add(Rectangle(pos=(0,0),size=self.size))
	
	def on_title(self,instance,value):
		self.t.text=value
		
	def on_body(self,instance,value):
		self.b.text=value
		
	def on_size(self,*args):
		self.draw()
			
	def __init__(self,**kwargs):
		super(GraphLabel,self).__init__(**kwargs)
		self.size_hint=(0.3,0.3)
		l=BoxLayout(size_hint=(1,1),orientation='vertical')
		self.t=MDLabel(text="",size_hint=(1,0.2),valign='top',halign='center')
		self.b=MDLabel(text="",size_hint=(1,0.8),valign='top')
		l.add_widget(self.t)
		l.add_widget(self.b)
		self.add_widget(l)