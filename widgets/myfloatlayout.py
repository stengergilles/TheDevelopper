from kivy.uix.floatlayout import FloatLayout


class MyFloatLayout(FloatLayout):

    def _child_exist(self,child=None):
        for i in self.children:
            if i == child:
               return True
        return False

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        pass

    def on_touch_down(self,touch):
        for i in self.children:
           if i.collide_point(*touch.pos):
              if self._child_exist(child=self.menu):
                 self.remove_widget(self.menu)
              return(i.on_touch_down(touch))
        if not self._child_exist(child=self.menu):
           self.add_widget(self.menu)
           self.menu.center_x=touch.pos[0]
           self.menu.center_y=touch.pos[1]
        else:
           for i in self.menu.children:
               if i.collide_point(*touch.pos):
                  return i.on_touch_down(touch)
           self.remove_widget(self.menu)

    def on_touch_up(self,touch):
        pass

    def on_touch_move(self,touch):
        pass

    def __init__(self,menu=None, **kwargs):
        super(MyFloatLayout, self).__init__(**kwargs)
        self.menu=menu