from kivy.graphics import Color, Canvas, Ellipse, Line, Rectangle
from data.dataobject import DataObject
from widgets.myfloatlayout import MyFloatLayout
from widgets.mygridlayout import MyGridLayout
from kivy.metrics import dp
from widgets.mylabel import MyLabel
from kivy.metrics import Metrics

def px2dp(px):
    return px/Metrics.density

class SchemaObject(MyFloatLayout):

    def _getstate(self):
        ret = {
            'icon': self.icon,
            'title': self.title.label.text,
            'pos': (px2dp(self.pos[0]), px2dp(self.pos[1])),
            'size': (px2dp(self.size[0]), px2dp(self.size[1])),
            'data': self.dataobject._getstate()
        }
        return ret

    def on_touch_down(self, touch):
        for i in self.children:
            if i.collide_point(*touch.pos):
               return i.on_touch_down(touch)
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
            self.pos = touch.pos
        return super().on_touch_move(touch)

    def redraw(self, object, pos):
        self.canvas.before.clear()
        txtlength = 0
        halfsize=(self.size[0]/2,self.size[1]/2)
        for i in self.children:
            if (hasattr(i, "tag")):
                if i.tag == "title":
                    i.texture_update()
                    i.pos = (self.pos[0] + halfsize[0], self.pos[1] + halfsize[1])
                    txtlength = i.label.texture.width / 2
            if type(i) is MyGridLayout:
                i.pos = (self.pos[0] + halfsize[0] + int(dp(2)), self.pos[1] - halfsize[1] - int(dp(16)))
        with self.canvas.before:
            Color(1.0, 1.0, 1.0)
            Line(points=(self.pos[0] + int(dp(12)), self.pos[1] + int(dp(12)), self.pos[0] + halfsize[0],
                         self.pos[1] + int(dp(12))))
            if hasattr(self, "icon"):
                Rectangle(pos=(self.pos[0] + int(dp(14)), self.pos[1] + int(dp(14))),
                          size=(halfsize[0] - int(dp(16)), halfsize[1] - int(dp(16))), source=self.icon)
            Line(points=(self.pos[0] + halfsize[0], self.pos[1] + int(dp(12)), self.pos[0] + halfsize[0],
                         self.pos[1] + halfsize[1]))
            Line(points=(self.pos[0] + halfsize[0], self.pos[1] + halfsize[1], self.pos[0] + halfsize[0] + txtlength,
                         self.pos[1] + halfsize[1]))
            Ellipse(pos=self.pos, size=(int(dp(24)), int(dp(24))))
            Color(0.0, 0.0, 0.0)
            Ellipse(pos=(int(self.pos[0] + dp(2)), int(self.pos[1] + dp(2))), size=(int(dp(20)), int(dp(20))))

def createSchemaObject(title=None, icon=None, dataobject=None):
    newWidget = SchemaObject()
    newWidget.canvas = Canvas()
    newWidget.title = MyLabel(text=title, font_size=14)
    newWidget.title.tag = "title"
    newWidget.add_widget(newWidget.title)
    newWidget.bind(pos=newWidget.redraw, size=newWidget.redraw)
    newWidget.size_hint = (None, None)
    newWidget.size = (int(dp(200)), int(dp(200)))
    if not icon is None:
        newWidget.icon = icon
    if not dataobject is None:
        newWidget.dataobject = dataobject
        newWidget.add_widget(newWidget.dataobject.getLayout())
    return newWidget


def deserialize(s=None):
    dataobject = DataObject()
    for k in s['data']['displayname'].keys():
        v = s['data']['fields'][k]
        setattr(dataobject, k, v)
        dataobject.addField(name=k, displayname=s['data']['displayname'][k])
    ret = createSchemaObject(title=s['title'], icon=s['icon'], dataobject=dataobject)
    ret.pos = s['pos']
#    ret.size = s['size']
    return ret
