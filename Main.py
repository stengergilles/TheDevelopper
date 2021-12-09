from kivy.app import App
from kivy.core import window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Canvas,Ellipse, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.vector  import Vector
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.utils import platform
from kivy.metrics import dp

from kivy_addons.CustomModules import CustomGraphics

from random import randint
import os 

def getUserPath():
    if platform == "win":
        return(os.getenv("USERPROFILE"))
    if platform == "linux": 
        return(os.getenv("HOME"))
    if platform == "android":
        try:
            from jnius import autoclass
            env = autoclass('android.os.Environment').getExternalStorageDirectory().getPath()
            return(env)
        except Exception as a:
            return(None)
	
class SettingSpacer(Widget):
    pass

class FileDialog:

    def _update(self,instance,others):
        value=self.fb.path.strip()
        if len(self.fb.selection):
        	value=os.path.join(value,self.fb.selection[0])
        setattr(self.sourceObject,self.sourceProperty,value)
        self.dirname.text=value

    def _dismiss(self,*args):
        if self.fb:
              self.fb.focus = False
        if self.popup:
              self.popup.dismiss()
        self._update(None,None)
        self.popup = None
        self.onsubmit()

    def _create(self,sourceObject=None,sourceProperty=None,title=None,onsubmit=None):
        self.onsubmit=onsubmit
        self.sourceProperty=sourceProperty
        self.sourceObject=sourceObject
        self.title=title
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = Popup(
            title=title, content=content, size_hint=(None, 0.9),
            width=popup_width,auto_dismiss=False)
        self.fb = FileChooserListView(
            path=getattr(self.sourceObject,self.sourceProperty), size_hint=(1, 1), dirselect=False)
        self.fb.layout.ids.scrollview.scroll_type=['bars']
        self.fb.layout.ids.scrollview.bar_width='10dp'
        self.fb.bind(path=self._update)
        self.dirname=Label(text=self.fb.path,size_hint_y=None)
        content.add_widget(self.dirname)
        content.add_widget(self.fb)
        content.add_widget(SettingSpacer())
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

    def __init__(self,sourceObject=None,sourceProperty=None,title=None,onsubmit=None):
        self._create(sourceObject=sourceObject,sourceProperty=sourceProperty,title=title,onsubmit=onsubmit)

    def showDialog(self):
        if self.popup is None:
            self._create(sourceObject=self.sourceObject,sourceProperty=self.sourceProperty,title=self.title,onsubmit=self.onsubmit)
        self.popup.open()

class CircularButton(ButtonBehavior,Widget):
    	
    def __init__(self,**kwargs):
        super(CircularButton,self).__init__(**kwargs)
        with self.canvas:
            Ellipse(pos=self.pos,size=self.size,source='16353994315461292131848351535886.png')

    def _resize(self):
    	self.size=(self.size[0]*2,self.size[1]*2)
        
    def on_press(self):
        self.size=(self.size[0]/2,self.size[1]/2)
        Clock.schedule_once(lambda dt:  self._resize(),1.0)
    	
    def collide_point(self,x,y):
        return Vector(x,y).distance(self.center)<=self.width/2

    def redraw(self,object,pos):
        self.canvas.before.clear()
        self.canvas.clear()
        with self.canvas.before:
            Color(1.0,1.0,1.0)
            Ellipse(pos=self.pos,size=self.size,source='16353994315461292131848351535886.png')

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

class SchemaApp(App):
    root=None
    menu=None

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
                i.pos=(window.width*0.8,20)

    def _loadCanvas(self):
        for i in self.root.children:
            if type(i) is SchemaObject:
                self.root.remove_widget(i)
        newWidget=SchemaObject()
        newWidget.canvas=Canvas()
        newWidget.add_widget(Label(text="my first object",halign="left",valign="top",pos=(0,0),text_size=(100,50)))
        newWidget.bind(pos=newWidget.redraw,size=newWidget.redraw)
        newWidget.size_hint=(0.1,0.1)
        newWidget.pos=(randint(50,100),randint(50,100))
        self.root.add_widget(newWidget)

    def build(self):
        self.root=FloatLayout(size=(Window.width,Window.height))
        CustomGraphics.SetBG(self.root,bg_color=[0.5,0.5,0.5,1])
        self.menu=CircularButton(pos=(Window.width*0.8,20),size=(64,64),size_hint=(None,None))
        self.menu.bind(pos=self.menu.redraw,size=self.menu.redraw,on_press=self._create_popup_workspace_open)
        self.root.add_widget(self.menu)
        self._loadCanvas()
        Window.bind(on_resize=self.on_window_resize)
        return self.root

if __name__ == '__main__':
    SchemaApp().run()