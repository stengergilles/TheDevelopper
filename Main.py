from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Canvas
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.metrics import dp

from kivy_addons.CustomModules import CustomGraphics

from random import randint

from tools.platform import getUserPath
from dialogs.files import FileDialog
from widgets.circularbutton import CircularButton
from app.schemaobject import SchemaObject
from app.schemaobject import createSchemaObject

class SchemaApp(App):
	racine=None
	principal=None
	ouvrir=None
	close=None
	scrollpos=(0,0)

	workspaceRoot = StringProperty(getUserPath())

	def _create_popup_workspace_ouvrir(self,event):
		if not hasattr(self, "ouvrirFile"):
			self.ouvrirFile = FileDialog(
				sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadCanvas)
		else:
			if self.ouvrirFile is None:
				self.ouvrirFile = FileDialog(
					sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadCanvas)
		self.ouvrirFile.showDialog()

	def _loadCanvas(self):
		for i in self.racine.children:
			if type(i) is SchemaObject:
				self.racine.remove_widget(i)
		newWidget=createSchemaObject(title='My First Object')
		newWidget.pos=(randint(50,100),randint(50,100))
		self.racine.add_widget(newWidget)

	def on_window_resize(self,window,width,height):
		for i in self.racine.children:
			if type(i) is CircularButton:
				i.pos=((1 - i.factor * i.size[0]/window.width)*window.width,20)

	def on_touch_down(self,floatlayout,touch):
		for i in self.racine.children:
			if i.collide_point(*touch.pos):
				return i.on_touch_down(touch)
		self.moving=True
		self.prevpos=touch.pos

	def on_touch_up(self,floatlayout,touch):
		for i in self.racine.children:
			if i.collide_point(*touch.pos):
				return i.on_touch_up(touch)	
		self.moving=False
		self.prevpos=None

	def on_touch_move(self,floatlayout,touch):
		for i in self.racine.children:
			if i.collide_point(*touch.pos):
				return i.on_touch_move(touch)		
		if self.moving:
			delta=((touch.pos[0]-self.prevpos[0]),(touch.pos[1]-self.prevpos[1]))
			self.prevpos=(touch.pos[0],touch.pos[1])
			for i in self.racine.children:
				if type(i) is SchemaObject:
					i.pos=(i.pos[0]+delta[0],i.pos[1]+delta[1])

	def build(self):
		self.racine=FloatLayout(size=(Window.width,Window.height))
		self.racine.bind(on_touch_down=self.on_touch_down,on_touch_up=self.on_touch_up,on_touch_move=self.on_touch_move)
		CustomGraphics.SetBG(self.racine,bg_color=[0.5,0.5,0.5,0.5])
		self.ouvrir=CircularButton(img='fileopen.png',pos=((1 - dp(64)/Window.width)*Window.width,dp(20)),size=(dp(64),dp(64)),size_hint=(None,None))
		self.ouvrir.factor=1
		self.ouvrir.bind(pos=self.ouvrir.redraw,size=self.ouvrir.redraw,on_press=self._create_popup_workspace_ouvrir)
		self.racine.add_widget(self.ouvrir)
		self.close=CircularButton(img='fileclose.png',pos=(int((1 - 2 * dp(64)/Window.width)*Window.width),int(dp(20))),size=(int(dp(64)),int(dp(64))),size_hint=(None,None))
		self.close.factor=2
		self.close.bind(pos=self.close.redraw,size=self.close.redraw)
		self.racine.add_widget(self.close)
		self._loadCanvas()
		Window.bind(on_resize=self.on_window_resize)
		return self.racine

if __name__ == '__main__':
	SchemaApp().run()
