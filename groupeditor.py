from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList,OneLineIconListItem,IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from mydialog import MyDialog
from kivy.metrics import dp
from kivy.properties import ObjectProperty

class EditGroupDialog(MyDialog):
	
	groupdata=ObjectProperty(None)
	
	def remove_child(self,*args):
		n=args[0].data
		self.groupdata._content.remove_widget(n)
		self.groupdata.parent.add_widget(n)
		self.groupdata._trigger()
		
	def on_groupdata(self,instance,value):
		for i in self.groupdata.walk(restrict=True):
			if not i is self.groupdata and isinstance(i,RelativeLayout):
				o=OneLineIconListItem(text=i.title)
				ic=IconLeftWidget(icon='minus')
				ic.data=i
				ic.bind(on_release=self.remove_child)
				o.add_widget(ic)
				self.members.add_widget(o)
	
	def count_items(self):
		if not self.groupdata:
			return 0,0
		c=0
		h=0
		for i in self.groupdata.walk(restrict=True):
			if not i is self.groupdata and isinstance(i,RelativeLayout) and hasattr(i,'title'):
				c=c+1
				h=i.height
		return c,h
		
	def myresize(self,instance,value):
		c,h=self.count_items()
		if 0<c<=3:
			self.root.height=h*(c+1)
			self.height=self.root.height+self.nodetitle.height
		else:
			if c==0:
				self.height=value[1]*4
	
	def __init__(self,**kwargs):
		super(EditGroupDialog,self).__init__(**kwargs)
		self.nodetitle=MDTextField(hint_text='Group Title')
		self.add_widget(self.nodetitle)
		self.root=ScrollView(size_hint=(1,None))
		self.members=MDList(size_hint=(1,None))
		self.members.bind(minimum_height=self.members.setter('height'))
		self.members.bind(size=self.myresize)
		self.root.add_widget(self.members)
		self.add_widget(self.root)