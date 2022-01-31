from dataclasses import dataclass
from tkinter import Widget
from turtle import title
from widgets.tools.stiffscrolleffect import StiffScrollEffect
from widgets.circularbutton import CircularButton
from widgets.mygridlayout import MyGridLayout
from widgets.mylabel import MyLabel
from widgets.mytextinput import MyTextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp 
from kivy.clock import Clock
from widgets.mydatagrid import DataGrid
import json

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

    def editorlayout(self,*args):
        editor=self.editordialog.children[0]
        if editor.size[0] != editor.parent.size[0]:
           editor.width=editor.parent.width
        titleblock=editor.children[1]
        titleblock.width=editor.width - dp(10)
        iconlabel=titleblock.children[1]
        iconblock=titleblock.children[0]
        iconbutton=iconblock.children[0]
        iconbutton.height=titleblock.row_height
        iconbutton.width=titleblock.row_height
        iconlabel.width=titleblock.col_width
        iconblock.width=titleblock.width - titleblock.col_width
        iconblock.height=titleblock.row_height
        datagrid=editor.children[0].children[0]
        datagrid.pos=(titleblock.pos[0],editor.height-datagrid.height-iconblock.height*2 - dp(5))

    def geteditor(self,size=None,pos=None):
        if hasattr(self,'editor'):
           return self.editor
        ret = ScrollView(do_scroll_x=False,do_scroll_y=True)
        ret.size_hint=(None,None)
        ret.pos_hint=(None,None)
        ret.effect_cls=StiffScrollEffect
        ret.always_overscroll=False
        ret.size=size
        ret.pos=pos
        editor=StackLayout()
        editor.size_hint=(None,None)
        editor.size=(size[0],size[1]*2)
        titleblock=self.getfield(label="Node Title")
        titleblock.add_widget(Label(text="Node Icon:",halign='right',font_size='12dp',size_hint=(None,None),width=titleblock.col_width ,height=titleblock.row_height))
        iconblock=BoxLayout(orientation='horizontal',size_hint=(None,None),size=(titleblock.width - titleblock.col_width,titleblock.row_height))
        iconblock.add_widget(TextInput(size_hint=(0.95,None),height=titleblock.row_height,font_size='12sp'))
        iconblock.add_widget(CircularButton(img="fileopen.png",size_hint=(None,None),width=titleblock.row_height,height=titleblock.row_height,on_press=showopeniconfile))
        titleblock.add_widget(iconblock)
        editor.add_widget(titleblock)
        ret.add_widget(editor)
        table=GridLayout(size=(size[0],size[1]*2),size_hint=(None,None))
        dg=DataGrid(['Name','Display Name','Type'],[0.2,1,0.2])
        dg.pos_hint=(None,None)
        dg.rows=1
        zz=[]
        i=0
        while i<50:
        	zz.append(['field'+str(i),'Field '+str(i),'str'])
        	i += 1
        for i in zz:
            dg.add_row(row_data=i,cols_size=[0.2,1,0.2],row_align=['center','center','center'])
        table.add_widget(dg)
        table.cols=1
        editor.add_widget(table)
        self.editordialog=ret
        Clock.schedule_once(self.editorlayout, 0.01)
        return ret