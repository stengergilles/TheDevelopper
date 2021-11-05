from kivy.utils import platform
import os

def getUserPath():
        if platform == "android":
        	try:
        		from jnius import autoclass
        		env = autoclass('android.os.Environment').getExternalStorageDirectory().getPath()
        		return(env)
        	except Exception as a:
        		return(None)
        if platform == "win":
        	return(os.getenv("USERPROFILE"))
        if platform == "linux":
        	return(os.getenv("HOME"))
        return(None)