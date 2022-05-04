from kivymd.app import MDApp

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager,SlideTransition
from kivy.utils import platform

from mainpanel import MainPanel

import commons

import os

import asyncio

import cProfile,pstats

class TheDevelopper(MDApp):
	
	def config_app(self):
		commons.init()
		if platform == 'android':
			from android import storage
			try:
				from android.permissions import request_permissions, Permission
				request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
			except:
				pass
			commons.start_dir=storage.primary_external_storage_path()
		if platform == 'linux':
			commons.start_dir=os.getenv('HOME')
		if platform == 'window':
			commons.start_dir=os.getenv('APPDATA')
		self.theme_cls.theme_style="Light"
		self.theme_cls.primary_palette="Blue"
		Window.softinput_mode='below_target'
	
	def makepanel(self,*args):
		if not type(args[0]) is str:
			s=Screen(name='schema1')
		else:
			s=Screen(name=args[0])
		self.root=MainPanel(app=self,pos=(0,0),size=(Window.width,Window.height),size_hint=(None,None))
		s.add_widget(self.root)
		self.sm.add_widget(s)
		if not type(args[0]) is str:
			self.sm.switch_to(s)
		else:
			return s,self.root
	
	def build(self):
		self.config_app()
		self.sm=ScreenManager(transition=SlideTransition())
		s=Screen(name='splash')
		s.add_widget(Image(source='icon.png'))
		self.sm.switch_to(s)
		Clock.schedule_once(self.makepanel)
		return(self.sm)
	
	def hook_keyboard(self,window,key,*largs):
		if platform == 'android':
			if key == 27:
				return True
		return False
		
	def on_start(self):
		if platform == 'android':
			from kivy.base import EventLoop
			EventLoop.window.bind(on_keyboard=self.hook_keyboard)
#		self.profile=cProfile.Profile()
#		self.profile.enable()
		
	def on_stop(self):
		Window.close()
#		self.profile.disable()
#		pstats.Stats(self.profile).sort_stats('tottime').print_stats(10)
		
if __name__ == '__main__':
	Window.maximize()
	Config.set('kivy','clock','free_only')
	Config.set('graphics','display','-1')
	Config.set('graphics','fullscreen','1')
	Config.set('graphics','height',str(Window.system_size[1]))
	Config.set('graphics','left','0')
	Config.set('graphics','top','0')
	Config.set('graphics','width',str(Window.system_size[0]))
	Config.set('graphics','resizable','0')
	Config.set('graphics','borderless','1')
	Config.set('graphics','window_state','visible')
	a=TheDevelopper()
	loop=asyncio.get_event_loop()
	loop.run_until_complete(a.async_run())
	loop.close()