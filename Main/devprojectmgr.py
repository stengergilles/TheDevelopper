from glob import glob
from os.path import dirname, join
from random import randint

from kivy.app import App
from kivy.logger import Logger
from kivy.properties import StringProperty
#kivy.require('1.0.6')
from kivy.uix.scatter import Scatter
from devdiagram import loadDevDiagram

import sys
sys.path.append("..")
sys.path.append(".")
from Lib.filedialog import FileDialog
from Lib import getUserPath  

class Project(Scatter):  
    source = StringProperty(None)
    
class ProjectApp(App):
    workspaceRoot=StringProperty(getUserPath())
    
    def on_workspaceRoot(self,instance,value):
    	self.root.ids.title.text=value
    	
    def _loadfile(self):
    	self.devdiagram=loadDevDiagram(name=self.workspaceRoot)
    
    def _create_popup_workspace_open(self):
        if not hasattr(self,"openFile"):
            self.openFile=FileDialog(sourceObject=self,sourceProperty="workspaceRoot",title="Open Schema",onsubmit=self._loadfile)
        else:
            if self.openFile is None:
                self.openFile=FileDialog(sourceObject=self,sourceProperty="workspaceRoot",title="Open Schema",onsubmit=self._loadfile)
        self.openFile.showDialog()
        
    def build(self):
    	value=getUserPath()
    	self.workspaceRoot=value
    	root = self.root
    	curdir = dirname(__file__)
    	for filename in glob(join(curdir, 'images', '*')):
            try:
                picture = Project(source=filename, rotation=randint(-30, 30))
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True

if __name__ == '__main__':
    ProjectApp().run()
