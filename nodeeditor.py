from field import Field
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from mydialog import MyDialog

class EditNodeDialog(MyDialog):
	
	nodedata=ObjectProperty(None)
	
	def on_nodedata(self,*args):
		for i in self.nodedata._form.walk(restrict=True):
			if type(i) is Field:
				self.add_item(i.t.helper_text)
				
	def count_members(self):
		c=0
		h=0
		for i in self.members.walk(restrict=True):
			if type(i) is MDTextField:
				c=c+1
				if i.height>h:
					h=i.height
		return c,h
		
	def remove_item(self,instance):
		self.members.remove_widget(instance.parent)
		self.nodedata._form.remove_field(instance.t.text)
		
	def add_item(self,*args):
		if args:
			if type(args[0]) is str:
				n=args[0]
			else:
				n=" "
		else:
			n=""
		c,h=self.count_members()
		a=BoxLayout(size_hint=(1,None),orientation='horizontal')
		if h==0:
			h=dp(48)
		a.height=h
		self.height=self.height+h
		self.parent.height=self.parent.height+h
		t=MDTextField(helper_text='Field Name',helper_text_mode='persistent',text=n)
		a.add_widget(t)
		b=MDIconButton(icon='minus',size_hint=(None,None),size=(dp(24),dp(24)))
		b.t=t
		b.bind(on_press=self.remove_item)
		a.add_widget(b)
		self.members.add_widget(a)
		
	def __init__(self,**kwargs):
		super(EditNodeDialog,self).__init__(**kwargs)
		self.height=dp(100)
		self.members=BoxLayout(size_hint=(1,None),orientation='vertical')
		self.members.height=dp(48)
		self.add_widget(self.members)
		self.nodetitle=MDTextField(hint_text='Node Title')
		self.add_widget(self.nodetitle)
		self.a=AnchorLayout(size_hint=(1,None))
		self.i=MDIconButton(icon='plus',size_hint=(None,None),size=(dp(24),dp(24)))
		self.i.bind(on_press=self.add_item)
		self.a.add_widget(self.i)
		self.add_widget(self.a)