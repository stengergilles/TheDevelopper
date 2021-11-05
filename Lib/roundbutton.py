from kivy.clock import Clock
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.vector  import Vector

class CircularButton(ButtonBehavior,Widget):
    	
    def _resize(self):
    	self.size=(self.size[0]*2,self.size[1]*2)
    	
    def on_press(self):
    	self.size=(self.size[0]/2,self.size[1]/2)
    	Clock.schedule_once(lambda dt:  self._resize(),1.0)
    	
    def collide_point(self,x,y):
        return Vector(x,y).distance(self.center)<=self.width/2