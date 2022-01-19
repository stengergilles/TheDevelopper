import os

from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.textinput import TextInput


class SettingSpacer(Widget):
    pass


class FileDialog:

    def _update(self, instance, others):
        value = self.fb.path.strip()
        if hasattr(self, "saveAs"):
            if os.path.isfile(value):
                value = os.path.dirname(value)
            if len(self.fb.selection) and not len(self.saveAs.text):
                value = os.path.join(value, self.fb.selection[0])
            if not len(self.fb.selection) and len(self.saveAs.text):
                value = os.path.join(value, self.saveAs.text)
        else:
            if len(self.fb.selection):
                value = os.path.join(value, self.fb.selection[0])
        setattr(self.sourceObject, self.sourceProperty, value)
        self.dirname.text = value

    def _dismiss(self, *args):
        if self.fb:
            self.fb.focus = False
        if self.popup:
            self.popup.dismiss(force=True)
        self.popup = None

    def _submit(self, *args):
        if self.fb:
            self.fb.focus = False
        if self.popup:
            self.popup.dismiss()
        self._update(None, None)
        self.popup = None
        self.onsubmit()

    def _create(self, sourceobject=None, sourceproperty=None, title=None, onsubmit=None, saveas=None):
        self.onsubmit = onsubmit
        self.sourceProperty = sourceproperty
        self.sourceObject = sourceobject
        self.title = title
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = Popup(
            title=title, content=content, size_hint=(None, 0.9),
            width=popup_width, auto_dismiss=False)
        self.fb = FileChooserListView(
            path=getattr(self.sourceObject, self.sourceProperty), size_hint=(1, 1), dirselect=False)
        self.fb.layout.ids.scrollview.scroll_type = ['bars']
        self.fb.layout.ids.scrollview.bar_width = '10dp'
        self.fb.bind(path=self._update)
        self.dirname = Label(text=self.fb.path, size_hint_y=None)
        content.add_widget(self.dirname)
        content.add_widget(self.fb)
        content.add_widget(SettingSpacer())
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._submit)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)
        if saveas:
            self.saveAs = TextInput(size_hint_y=None, height='50dp')
            content.add_widget(self.saveAs)

    def __init__(self, sourceobject=None, sourceproperty=None, title=None, onsubmit=None, saveas=None):
        self._create(sourceobject=sourceobject, sourceproperty=sourceproperty, title=title, onsubmit=onsubmit,
                     saveas=saveas)

    def showdialog(self,*args):
        if self.popup is None:
            self._create(sourceobject=self.sourceObject, sourceproperty=self.sourceProperty, title=self.title,
                         onsubmit=self.onsubmit)
        self.popup.open()