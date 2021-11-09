from kivy.properties import StringProperty
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.core.window import Window

class SchemaObject(Scatter):
    source = StringProperty(None)

def cleanUi():
	pass
	
def createUiGraph(g=None):
	for i in g:
		newWidget=SchemaObject()
		newWidget.ids.title.text=i.className
		App.get_running_app().root.add_widget(newWidget)