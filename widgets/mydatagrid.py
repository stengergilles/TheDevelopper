from turtle import bgcolor
from kivy.lang.builder import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from functools import partial

Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
                    )


class CLabel(ToggleButton):
    bgcolor = ListProperty()


class HeaderLabel(Label):
    bgcolor = ListProperty()


class DataGrid(GridLayout):
    def __init__(self, header_data, cols_size, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.rows = 0
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.cols = len(header_data)
        self.spacing = [0, 0]
        self.counter = 0
        n = 0
        for hcell in header_data:
            header_str = "[b]" + str(hcell) + "[/b]"
            h=HeaderLabel(bgcolor=[0.108,0.476,0.611])
            h.text=header_str
            h.markup=True
            h.size_hint_y=None
            h.height=40
            h.id="Header_Label"
            h.size_hint_x=cols_size[n]
            h.bgcolor=[0.108,0.476,0.611]
            self.add_widget(h)
            n += 1

    def add_row(self, row_data, row_align, cols_size):
        self.rows += 1

        def change_on_press(clabel):
            childs = clabel.parent.children
            for ch in childs:
                if ch.id == clabel.id:
                    row_n = ch.id[4:5] if len(ch.id) == 11 else ch.id[4:6]
                    for c in childs:
                        if ('row_' + str(row_n) + '_col_') in c.id:
                            change_on_release(c)

        def change_on_release(clabel):
            clabel.state = "down" if clabel.state == "normal" else "normal"

        n = 0
        for item in row_data:
            cell = CLabel(text=('[color=000000]' + item + '[/color]'),bgcolor=[1,1,1])
            cell.background_color_normal=ListProperty([1, 1, 1, 0.5])
            cell.background_color_down = ListProperty([1, 1, 1, 1])
            cell.halign=row_align[n]
            cell.markup=True
            cell.bind(on_press=change_on_press,on_release=change_on_release)
            cell.text_size=(0, None)
            cell.size_hint_x=cols_size[n]
            cell.size_hint_y=None
            cell.height=40
            cell.id=("row_" + str(self.counter) + "_col_" + str(n))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size = (cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n += 1
        self.counter += 1

    def remove_row(self, n_cols, instance, **kwargs):
        childs = self.parent.children
        selected = 0
        for ch in childs:
            for c in reversed(ch.children):
                if c.id != "Header_Label":
                    if c.state == "down":
                        self.remove_widget(c)
                        selected += 1
        if selected == 0:
            for ch in childs:
                count = 0
                while count < n_cols:
                    if n_cols != len(ch.children):
                        for c in ch.children:
                            if c.id != "Header_Label":
                                self.remove_widget(c)
                                count += 1
                                break
                            else:
                                break
                    else:
                        break

    def select_all(self, instance, **kwargs):
        self.change_state("down")

    def unselect_all(self, instance, **kwargs):
        self.change_state("normal")

    def change_state(self, state):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = state
