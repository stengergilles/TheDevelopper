from widgets.mygridlayout import MyGridLayout
from widgets.mylabel import MyLabel
from widgets.mytextinput import MyTextInput


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
