from kivy.uix.floatlayout import FloatLayout
from app.menu import Menu
from app.schemaobject import SchemaObject


class MainPanel(FloatLayout):

    def my_touch_down(self, object, touch):
        for i in object.walk(restrict=True):
            if i.collide_point(*touch.pos) and not i is object:
                return i.dispatch('on_touch_down', touch)
        if touch.is_double_tap:
            object.m.center_x = touch.pos[0]
            object.m.center_y = touch.pos[1]
            if not object.m.visible:
                object.m.visible = True
                object.add_widget(object.m)
                return True
        else:
            self.moving = True
        return False

    def my_touch_move(self, object, touch):
        if object.moving:
            for i in object.walk(restrict=True):
                if isinstance(i, SchemaObject):
                    i.pos = (i.pos[0]+touch.dx, i.pos[1]+touch.dy)
            return True
        return False

    def my_touch_up(self, object, touch):
        if object.moving:
            object.moving = False
            return True
        return False

    def __init__(self, menu=None, **kwargs):
        super(MainPanel, self).__init__(**kwargs)
        self.moving = False
        self.m = Menu(data=menu, pos=(200, 200))
        self.bind(on_touch_down=self.my_touch_down,
                  on_touch_move=self.my_touch_move, on_touch_up=self.my_touch_up)
