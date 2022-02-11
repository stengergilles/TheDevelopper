from kivymd.uix.textfield import TextInput
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.metrics import dp

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class TypeList(TextInput):
	
	def set_item(self,item):
		self.text=item
		self.menu.dismiss()
		
	def openmenu(self,*args):
		if self.focus:
			self.menu.open()
	
	def __init__(self,**kwargs):
		super(TypeList,self).__init__(**kwargs)
		menu_items = [
		{ "viewclass": "IconListItem","icon": "git","height": dp(56),"text": f"String","on_release": lambda x=f"String": self.set_item(x)
		},
		{ "viewclass": "IconListItem","icon": "git","height": dp(56),"text": f"Integer","on_release": lambda x=f"Integer": self.set_item(x)
		},
		{ "viewclass": "IconListItem","icon": "git","height": dp(56),"text": f"Float","on_release": lambda x=f"Float": self.set_item(x)
		},
		{ "viewclass": "IconListItem","icon": "git","height": dp(56),"text": f"Boolean","on_release": lambda x=f"Boolean": self.set_item(x)
		}
		
		]
		self.menu = MDDropdownMenu(caller=self,items=menu_items,position="auto",width_mult=4)
		self.bind(focus=self.openmenu)
	