from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from kivy.config import Config

from mainpanel import MainPanel
from graphnode import GraphNode
from groupnode import GroupNode

import commons

import os

import asyncio
import logging

import cProfile,pstats
from pstats import SortKey

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
	
	def makepanel(self):
		self.root=MainPanel(app=self,pos=(0,0),size=(Window.width,Window.height),size_hint=(None,None))
		return(self.root)
	
	def build(self):
		self.config_app()
		return(self.makepanel())
		
#	def on_start(self):
#		self.profile=cProfile.Profile()
#		self.profile.enable()
		
#	def on_stop(self):
#		self.profile.disable()
#		pstats.Stats(self.profile).sort_stats('tottime').print_stats(10)
		
if __name__ == '__main__':
	Config.set('kivy','clock','free_only')
	a=TheDevelopper()
	loop=asyncio.get_event_loop()
	loop.run_until_complete(a.async_run())
	loop.close()