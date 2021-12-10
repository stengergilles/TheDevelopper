from kivy.graphics import Color,Canvas,Ellipse,Line,Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import sp,dp
from widgets.mylabel import MyLabel

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
		return super().on_touch_move(touch)

	def redraw(self,object,pos):
		self.canvas.before.clear()
		txtlength=0
		for i in self.children:
			if (hasattr(i,"tag")):
				if i.tag == "title":
					i.texture_update()
					i.pos=(self.pos[0]+self.size[0],self.pos[1]+self.size[1])
					txtlength=i.label.texture.width/2
		with self.canvas.before:
			Color(1.0,1.0,1.0)
			Line(points=(self.pos[0]+int(dp(12)),self.pos[1]+int(dp(12)),self.pos[0]+self.size[0],self.pos[1]+int(dp(12))))
			Line(points=(self.pos[0]+self.size[0],self.pos[1]+int(dp(12)),self.pos[0]+self.size[0],self.pos[1]+self.size[1]))
			Line(points=(self.pos[0]+self.size[0],self.pos[1]+self.size[1],self.pos[0]+self.size[0]+txtlength,self.pos[1]+self.size[1]))
			Ellipse(pos=self.pos,size=(int(dp(24)),int(dp(24))))
			Color(0.0,0.0,0.0)
			Ellipse(pos=(int(self.pos[0]+dp(2)),int(self.pos[1]+dp(2))),size=(int(dp(20)),int(dp(20))))

def createSchemaObject(title=None):
	newWidget=SchemaObject()
	newWidget.canvas=Canvas()
	newWidget.title=MyLabel(text=title,font_size=sp(14))
	newWidget.title.tag="title"
	newWidget.add_widget(newWidget.title)
	newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
	newWidget.size_hint=(None,None)
	newWidget.size=(int(dp(100)),int(dp(100)))
	return newWidget