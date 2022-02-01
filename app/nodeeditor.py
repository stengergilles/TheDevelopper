from app.schemaobject import SchemaObject
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.toolbar import MDToolbar

class NodeEditor(SchemaObject):
	
	def __init__(self,data=None,**kwargs):
		super(NodeEditor,self).__init__(data=data,**kwargs)
		dt=MDDataTable(
			use_pagination=False,
			check=True,
			column_data=[
				("Name",dp(30)),
				("Display Name",dp(30)),
				("Type",dp(30))
			],
			row_data=self.data
		)
		tb=MDToolbar()
		tb.title="Node Editor"
		self.content=MDStackLayout()
		self.content.add_widget(dt)
		self.content.add_widget(tb)
		self.content.size=self.size
		self.content.pos=self.pos
		self.add_widget(self.content)
