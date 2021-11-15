from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color,Rectangle,Canvas,Ellipse, Line
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from random import randint
def cleanUi():
	for i in App.get_running_app().root.children:
		App.get_running_app().root.remove_widget(i)
	
def createUiGraph(g=None):
	for i in g:
		newWidget=SchemaObject()
		newWidget.canvas=Canvas()
		newWidget.add_widget(Label(text=i.className,halign="left",valign="top",pos=(0,0)))
		newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
		newWidget.size_hint=(0.1,0.1)
		newWidget.pos=(randint(50,100),randint(50,100))
		App.get_running_app().root.add_widget(newWidget)

class SchemaObject(FloatLayout):

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
				i.pos=(self.pos[0]+20, self.pos[1]+50)
		return super().on_touch_move(touch)

	def redraw(self,object,pos):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(1.0,1.0,1.0)
			Line(points=(self.x,self.y,self.x+self.width,self.y))
			Line(points=(self.x+self.width,self.y,self.x+self.width,self.y+self.height))
			Ellipse(pos=self.pos,size=(24,24))
			Color(0.0,0.0,0.0)
			Ellipse(pos=(self.pos[0]+2,self.pos[1]+2),size=(20,20))