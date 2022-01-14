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

import os

class SchemaApp(App):
    root = None
    mainmenu = None

    workspaceRoot = StringProperty(getUserPath())

    def _savecanvas(self):
        if len(self.workspaceRoot):
            if os.path.isfile(self.workspaceRoot):
                save(fname=self.workspaceRoot, root=self.root, tosave=SchemaObject)

    def _loadcanvas(self):
        if len(self.workspaceRoot):
            if isjson(self.workspaceRoot):
                for i in self.root.children:
                    if type(i) is SchemaObject:
                        self.root.remove_widget(i)
                load(fname=self.workspaceRoot, root=self.root, toload=deserialize_schemaobject)
            else:
                if os.path.isfile(self.workspaceRoot):
                    self.workspaceRoot = os.path.dirname(self.workspaceRoot)

    def add_node(self, *args):
        pass

    def build(self):
        self.title = "Schema Editor"
        fileopen = CircularButton(img='fileopen.png', size=(dp(32), dp(32)), size_hint=(None, None),
                                  on_press=FileDialog(sourceobject=self, sourceproperty="workspaceRoot", title="Open Schema",
                                  onsubmit=self._loadcanvas).showdialog)
        close = CircularButton(img='fileclose.png', size=(dp(32), dp(32)), size_hint=(None, None),
                               on_press=FileDialog(sourceobject=self, sourceproperty="workspaceRoot", title="Save Schema",
                               onsubmit=self._savecanvas, saveas=True).showdialog)
        addnode = CircularButton(img='addnode.png', size=(dp(32), dp(32)), size_hint=(None, None),
                                 on_press=self.add_node)
        self.mainmenu = MyCircularLayout(degree_spacing=80, pos=(100, 100), size=(dp(100), dp(100)))
        self.mainmenu.size_hint = (None, None)
        self.mainmenu.add_widget(fileopen)
        self.mainmenu.add_widget(close)
        self.mainmenu.add_widget(addnode)
        self.root = MyFloatLayout(menu=self.mainmenu, size=(Window.width, Window.height))
        CustomGraphics.SetBG(self.root, bg_color=[0.5, 0.5, 0.5, 0.5])
        return self.root


if __name__ == '__main__':
    SchemaApp().run()
