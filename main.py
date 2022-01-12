from kivy.app import App
from widgets.myfloatlayout import MyFloatLayout
from widgets.mycircularlayout import MyCircularLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.metrics import dp

from kivy_addons.CustomModules import CustomGraphics

from tools.platform import getUserPath
from dialogs.files import FileDialog
from widgets.circularbutton import CircularButton
from app.schemaobject import SchemaObject
from app.schemaobject import deserialize as deserialize_schemaobject
from tools.files import isjson
from tools.files import save
from tools.files import load


class SchemaApp(App):
    root = None
    open = None
    close = None
    bubble = None
    moving = None
    prevpos = None

    workspaceRoot = StringProperty(getUserPath())

    def _create_popup_workspace_open(self, *args):
        if not hasattr(self, "openFile"):
            self.openFile = FileDialog(
                sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadcanvas)
        else:
            if self.openFile is None:
                self.openFile = FileDialog(
                    sourceObject=self, sourceProperty="workspaceRoot", title="Open Schema", onsubmit=self._loadcanvas)
        self.openFile.showDialog()

    def _create_popup_workspace_save(self, *args):
        if not hasattr(self, "saveFile"):
            self.saveFile = FileDialog(
                sourceObject=self, sourceProperty="workspaceRoot", title="Save Schema", onsubmit=self._savecanvas)
        else:
            if self.openFile is None:
                self.saveFile = FileDialog(
                    sourceObject=self, sourceProperty="workspaceRoot", title="Save Schema", onsubmit=self._savecanvas)
        self.saveFile.showDialog()

    def _savecanvas(self):
        # Check if isDirectory
        save(fname=self.workspaceRoot, root=self.root, tosave=SchemaObject)

    def _loadcanvas(self):
        if isjson(self.workspaceRoot):
            for i in self.root.children:
                if type(i) is SchemaObject:
                    self.root.remove_widget(i)
            load(fname=self.workspaceRoot, root=self.root, toload=deserialize_schemaobject)

    def on_window_resize(self, window, width, height):
        for i in self.root.children:
            if type(i) is CircularButton:
                i.pos = ((1 - i.factor * i.size[0] / width) * width, 20)

    def on_touch_down(self, touch, event):
        for i in self.root.children:
            if i.collide_point(*event.pos):
                ret = i.on_touch_down(event)
                if type(i) is MyCircularLayout:
                    self.root.remove_widget(self.bubble)
                return ret
        self.root.add_widget(self.bubble)
        self.bubble.pos = event.pos
        self.moving = True
        self.prevpos = touch.pos

    def on_touch_up(self, touch, *args):
        for i in self.root.children:
            if i.collide_point(*touch.pos):
                return i.on_touch_up(touch)
        self.moving = False
        self.prevpos = None

    def on_touch_move(self, touch, *args):
        for i in self.root.children:
            if i.collide_point(*touch.pos):
                return i.on_touch_move(touch)
        if hasattr(self, "moving"):
            if self.moving:
                delta = ((touch.pos[0] - self.prevpos[0]), (touch.pos[1] - self.prevpos[1]))
                self.prevpos = (touch.pos[0], touch.pos[1])
                for i in self.root.children:
                    if type(i) is SchemaObject:
                        i.pos = (i.pos[0] + delta[0], i.pos[1] + delta[1])

    def build(self):
        self.title = "Schema Editor"
        self.root = MyFloatLayout(size=(Window.width, Window.height))
        self.root.bind(on_touch_down=self.on_touch_down, on_touch_up=self.on_touch_up, on_touch_move=self.on_touch_move)
        CustomGraphics.SetBG(self.root, bg_color=[0.5, 0.5, 0.5, 0.5])
        self.open = CircularButton(img='fileopen.png', size=(dp(32), dp(32)), size_hint=(None, None))
        self.open.factor = 1
        self.open.bind(pos=self.open.redraw, size=self.open.redraw, on_press=self._create_popup_workspace_open)
        self.close = CircularButton(img='fileclose.png',size=(dp(32), dp(32)), size_hint=(None, None))
        self.close.factor = 2
        self.close.bind(pos=self.close.redraw, size=self.close.redraw, on_press=self._create_popup_workspace_save)
        Window.bind(on_resize=self.on_window_resize)
        self.bubble = MyCircularLayout(degree_spacing=80, pos=(100, 100), size=(dp(100), dp(100)))
        self.bubble.size_hint = (None, None)
        self.bubble.add_widget(self.open)
        self.bubble.add_widget(self.close)
        return self.root


if __name__ == '__main__':
    SchemaApp().run()
