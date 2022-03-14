from app.schemaobject import SchemaObject
from kivy.graphics import Line,Color,Rectangle
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp

class SchemaGroup(SchemaObject):
	
	def sethorizontal(self):
		if self.size[0]<self.size[1]:
			self.size=(self.size[1],self.size[0])
		Clock.schedule_once(self.redraw,0.005)
	
	def setvertical(self):
		if self.size[1]<self.size[0]:
			self.size=(self.size[1],self.size[0])
		Clock.schedule_once(self.redraw,0.005)
	
	def layout(self):
		startpos=(dp(5),dp(5))
		totalwidth=dp(5)
		maxheight=0
		myheight=0
		maxwidth=self.parent.size[0]
		interval=dp(5)
		for i in self.data['nodelist']:
			if interval+i.size[0]+totalwidth < maxwidth*0.3:
				i.pos=startpos
				totalwidth=totalwidth+i.size[0]
				startpos=(startpos[0]+i.size[0]+interval,startpos[1])
				if i.height+interval>maxheight:
					maxheight=i.height+interval
			else:
				startpos=(dp(5),startpos[1]+maxheight)
				myheight=myheight+maxheight
				maxheight=0
				totalwidth=dp(5)
				i.pos=startpos
		self.size=(maxwidth*0.3,myheight+maxheight)
		if self.ff:
			self.ff=False
			x=App.get_running_app().theme_cls.primary_color
			self.canvas.before.add(Color(x[0],x[1],x[2],x[3]))
			self.canvas.before.add(Rectangle(pos=(0,0),size=self.size))
					
	def redraw(self,*args):
		self.layout()
		
	def __init__(self,data=None,**kwargs):
		super(SchemaGroup,self).__init__(data=data,**kwargs)
		self.size_hint=(None,None)
		self.ff=True
		Clock.schedule_once(self.redraw,0.005)
		
	def addNode(self,s=None):
		if not 'nodelist' in self.data:
			self.data['nodelist']=[]
		self.data['nodelist'].append(s)
		s.filter=True
		s.parent.remove_widget(s)
		self.add_widget(s)
		Clock.schedule_once(self.redraw,0.005)