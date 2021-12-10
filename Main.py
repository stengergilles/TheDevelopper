from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
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
	root=None
	open=None
	close=None

	workspaceRoot = StringProperty(getUserPath())

	def _create_popup_workspace_open(self,event):
		if not hasattr(self, "openFile"):
			self.openFile = FileDialog(
				sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadCanvas)
		else:
			if self.openFile is None:
				self.openFile = FileDialog(
					sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadCanvas)
		self.openFile.showDialog()

	def on_window_resize(self,window,width,height):
		for i in self.root.children:
			if type(i) is CircularButton:
				i.pos=((1 - i.factor * i.size[0]/window.width)*window.width,20)

	def _loadCanvas(self):
		for i in self.root.children:
			if type(i) is SchemaObject:
				self.root.remove_widget(i)
		newWidget=createSchemaObject(title='My First Object')
		newWidget.pos=(randint(50,100),randint(50,100))
		self.root.add_widget(newWidget)

	def build(self):
		self.root=FloatLayout(size=(Window.width,Window.height))
		CustomGraphics.SetBG(self.root,bg_color=[0.5,0.5,0.5,1])
		self.open=CircularButton(img='fileopen.png',pos=((1 - dp(64)/Window.width)*    Window.width,dp(20)),size=(dp(64),dp(64)),size_hint=(None,None))
		self.open.factor=1
		self.open.bind(pos=self.open.redraw,size=self.open.redraw,on_press=self._create_popup_workspace_open)
		self.root.add_widget(self.open)
		self.close=CircularButton(img='fileclose.png',pos=(int((1 - 2 * dp(64)/Window.width)*Window.width),int(dp(20))),size=(int(dp(64)),int(dp(64))),size_hint=(None,None))
		self.close.factor=2
		self.close.bind(pos=self.close.redraw,size=self.close.redraw)
		self.root.add_widget(self.close)
		self._loadCanvas()
		Window.bind(on_resize=self.on_window_resize)
		return self.root

if __name__ == '__main__':
	SchemaApp().run()