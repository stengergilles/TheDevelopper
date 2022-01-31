from app.schemaobject import SchemaObject
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable

class NodeEditor(SchemaObject):
	
	def __init__(self,data=None,**kwargs):
		super(NodeEditor,self).__init__(data=data,**kwargs)
		self.content=MDDataTable(
			use_pagination=False,
			check=True,
			column_data=[
				("Name",dp(30)),
				("Display Name",dp(30)),
				("Type",dp(30))
			],
			row_data=self.data
		)
		self.content.size=self.size
		self.content.pos=self.pos
		self.add_widget(self.content)
