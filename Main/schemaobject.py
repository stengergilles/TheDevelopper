from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Canvas
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.app import App
from kivy.core.window import Window

class SchemaObject(Widget):
    
    def on_touch_move(self,touch):
    	self.pos=touch.pos
    	
    def redraw(self,*args):
    	with self.canvas:
    		c=Color(1.,1.,1.)
    		Rectangle(pos=self.pos,size=self.size)
	
def cleanUi():
	pass
	
def createUiGraph(g=None):
	for i in g:
		newWidget=SchemaObject()
#		newWidget.add_widget(Label(text=i.className))
		newWidget.size_hint=(0.1,0.1)
		newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
		App.get_running_app().root.add_widget(newWidget)