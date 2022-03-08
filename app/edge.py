from enum import Enum
from app.schemaobject import SchemaObject
from kivy.graphics import Triangle,Line,Color,Rectangle
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp

class SchemaEdge(SchemaObject):
		
	def drawArrow(self,p=None,dx=None,dy=None):
		cos=0.866
		sin=0.5
		end1=(p[0]+dx*cos+dy*-sin,p[1]+dx*sin+dy*cos)
		end2=(p[0]+dx*cos+dy*sin,p[1]+dx*-sin+dy*cos)
		return Triangle(points=(p[0],p[1],end1[0],end1[1],end2[0],end2[1]))
				
	def redraw(self, *args):
		if self.data['src'] and self.data['dst']:
			self.data['src'].create()
			self.data['dst'].create()
			cs=self.data['src'].c.size[0]/2
			ss=max(self.size[0],self.size[1])*0.01
			t1=None
			t2=None
			src=self.data['src'].to_parent(self.data['src'].c.center_x,self.data['src'].c.center_y)
			dst=self.data['dst'].to_parent(self.data['dst'].c.center_x,self.data['dst'].c.center_y)
			self.size=(abs(self.data['dst'].c.center_x-self.data['src'].c.center_x),abs(self.data['dst'].c.center_y-self.data['dst'].c.center_y))
			self.pos=(min(self.data['src'].c.center_x,self.data['dst'].c.center_x),min(self.data['src'].c.center_y,self.data['dst'].c.center_y))
			src=self.to_widget(*src)
			dst=self.to_widget(*dst)
			if self.l:
				self.canvas.before.remove(self.l)
			else:
				x=App.get_running_app().theme_cls.primary_color
				self.canvas.before.add(Color(x[0],x[1],x[2],x[3]))
			dx=(dst[0]-src[0])
			dy=(dst[1]-src[1])
			if dx>0:
				src=(src[0]+cs,src[1])
				dst=(dst[0]-cs,dst[1])
			else:
				src=(src[0]-cs,src[1])
				dst=(dst[0]+cs,dst[1])
			if dy>0:
				src=(src[0],src[1]+cs)
				dst=(dst[0],dst[1]-cs)
			else:
				src=(src[0],src[1]-cs)
				dst=(dst[0],dst[1]+cs)
			dx=(dst[0]-src[0])*0.1
			dy=(dst[1]-src[1])*0.1
			if self.data['dir']==1:
				t1=self.drawArrow(dst,-dx,-dy)
			else:
				if self.data['dir']==2:
					t1=self.drawArrow(src,dx,dy)
				else:
					if self.data['dir']==3:
						t1=self.drawArrow(src,dx,dy)
						t2=self.drawArrow(dst,-dx,-dy)
			if self.p1:
				self.canvas.before.remove(self.p1)
				self.p1=None
			if self.p2:
				self.canvas.before.remove(self.p2)
				self.p2=None
			if t1:
				self.p1=t1
				self.canvas.before.add(self.p1)
			if t2:
				self.p2=t2
				self.canvas.before.add(self.p2)
			self.l=Line(points=[src,dst])
			self.canvas.before.add(self.l)
		return super().redraw(*args)
		
	def resolve(self,d=None):
		for i in App.get_running_app().panel.walk(restrict=True):
			if isinstance(i,SchemaObject):
				if d == i.data['uuid']['hex']:
					return(i)
		return(None)
	
	def __init__(self,data=None,src=None,dst=None,dir=None,**kwargs):
		super(SchemaEdge,self).__init__(data=data,**kwargs)
		self.l=None
		self.p1=None
		self.p2=None
		self.filter=True
		if dir:
			data['dir']=dir
		if not 'dir' in data:
			data['dir']=4
		data['type']=type(self)
		if 'src' in data:
			if data['src'] is None:
				data['src']=src
			else:
				data['src']=self.resolve(data['src'])
		else:
			data['src']=src
		if 'dst' in data:
			if data['dst'] is None:
				data['dst']=dst
			else:
				data['dst']=self.resolve(data['dst'])
		else:
			data['dst']=dst
		if not hasattr(data['src'],'wantlink'):
			data['src'].wantlink=[]
		data['src'].wantlink.append(data['dst'])
		if not hasattr(data['src'].wantlink[-1],'e'):
			data['src'].wantlink[-1].e=[]
		data['src'].wantlink[-1].e.append(self)
		if not hasattr(data['dst'],'wantlink'):
			data['dst'].wantlink=[]
		data['dst'].wantlink.append(data['src'])
		if not hasattr(data['dst'].wantlink[-1],'e'):
			data['src'].wantlink[-1].e=[]
		data['dst'].wantlink[-1].e.append(self)
		self.direction=dir
		self.menuvisible=False
		Clock.schedule_once(self.redraw,0.005)