from tkinter import Grid
from turtle import title, width
from typing import Text
from widgets.circularbutton import CircularButton
from widgets.mygridlayout import MyGridLayout
from widgets.mylabel import MyLabel
from widgets.mytextinput import MyTextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp 

def showopeniconfile(*args):
	pass

class DataObject(object):
    displayname = None

    def _getstate(self):
        ret = {
            'displayname': self.displayname,
            'fields': {}
        }
        for k in self.displayname.keys():
            ret['fields'][k] = getattr(self, k).text
        return ret

    def getstate(self):
        return self._getstate()

    def __init__(self):
        self.displayname = {}

    def addfield(self, name=None, displayname=None):
        self.displayname[name] = displayname

    def getlayout(self):
        ret = MyGridLayout(size_hint=(None, 1))
        ret.cols = 2
        w = 0
        h = 0
        for i in self.displayname.keys():
            line = MyLabel(text=self.displayname[i], size_hint_y=None, size_hint_x=None, font_size=12)
            line.texture_update()
            line.size = (line.texture_size[0] * 1.2, line.texture_size[1] * 2)
            ret.add_widget(line)
            t = MyTextInput(multiline=False, size_hint_y=None, size_hint_x=None, font_size='12dp')
            t.text = getattr(self, i)
            setattr(self, i, t)
            texture = t._create_line_label("xxxxxxxxxx")
            ret.add_widget(t)
            if line.texture_size[1] + texture.size[0] > w:
                w = line.texture_size[1] + texture.size[0]
            t.size = (texture.size[0] * 1.4, line.texture_size[1] * 1.8)
            h += line.texture_size[1]
        ret.size = (w * 1.20, h)
        return ret

    def getfield(self,label=None):
        ret=GridLayout()
        ret.size_hint=(1,None)
        ret.cols=2
        title=Label(text=label+":",font_size='12dp',halign='right')
        title.size_hint=(None,None)
        title.texture_update()
        title.height=title.texture_size[1] + dp(2)
        title.width=title.texture_size[0] + dp(2)
        ret.add_widget(title)
        field=TextInput(font_size='12dp')
        field.padding=[0]
        field.multiline=False
        field.size_hint=(1,None)
        field.height=title.height
        ret.row_default_height=title.height
        ret.add_widget(field)
        ret.row_height=title.height
        ret.col_width=title.width
        return ret

    def geteditor(self,size=None,pos=None):
        ret = ScrollView(do_scroll_x=False,do_scroll_y=True)
        ret.size_hint=(None,None)
        ret.pos_hint=(None,None)
        ret.size=size
        ret.pos=pos
        editor=StackLayout()
        titleblock=self.getfield(label="Node Title")
        titleblock.add_widget(Label(text="Node Icon:",halign='right',font_size='12dp',size_hint=(None,None),width=titleblock.col_width ,height=titleblock.row_height))
        iconblock=StackLayout()
        iconblock.orientation='lr-tb'
        iconblock.size_hint=(None,None)
        iconblock.width=titleblock.width - titleblock.col_width
        iconblock.height=titleblock.row_height
        iconblock.add_widget(TextInput(size_hint=(None,None),width=iconblock.width * 0.5,height=titleblock.row_height,font_size='12sp'))
        iconblock.add_widget(CircularButton(img="fileopen.png",size_hint=(1,None),height=titleblock.row_height,on_press=showopeniconfile))
        titleblock.add_widget(iconblock)
        editor.add_widget(titleblock)
        ret.add_widget(editor)
        return ret