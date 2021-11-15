from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.app import App

def cleanUi():
	pass
	
def createUiGraph(g=None):
	for i in g:
		newWidget=SchemaObject()
		newWidget.add_widget(Label(text=i.className))
		newWidget.size_hint=(0.1,0.1)
		newWidget.pos=(100,100)
		newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
		App.get_running_app().root.add_widget(newWidget)

class SchemaObject(Widget):

	def on_touch_move(self, touch):
		self.pos=touch.pos
		return super().on_touch_move(touch)

	def redraw(self,object,pos):
		self.canvas.clear()
		with self.canvas:
			Color(1.0,1.0,1.0)
			Rectangle(pos=self.pos,size=self.size)