from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color,Rectangle,Canvas
from kivy.app import App
from random import randint
def cleanUi():
	pass
	
def createUiGraph(g=None):
	for i in g:
		newWidget=SchemaObject()
		newWidget.canvas=Canvas()
		newWidget.add_widget(Label(text=i.className))
		newWidget.size_hint=(0.1,0.1)
		newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
		newWidget.pos=(randint(50,100),randint(50,100))
		App.get_running_app().root.add_widget(newWidget)

class SchemaObject(Widget):

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			touch.grab(self)
			return True
		return super().on_touch_down(touch)

	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
		return super().on_touch_up(touch)

	def on_touch_move(self, touch):
		if touch.grab_current is self: 
			self.pos=touch.pos
			for i in self.children:
				i.pos=touch.pos
		return super().on_touch_move(touch)

	def redraw(self,object,pos):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(1.0,1.0,1.0)
			Rectangle(pos=self.pos,size=self.size)