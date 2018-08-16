# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
import base64
import platform
import sys
import os
import threading

def main():
	check_versions()
	sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
	
	settings = {
		"remote_debugging_port": 49152,
		# "resources_dir_path" : os.path.abspath('./')
	}

	cef.Initialize(settings=settings)

	# Note that the path is relative 
	browser = cef.CreateBrowserSync(url='file:///html/index.html',
									window_title="1. Local File")

	cef.MessageLoop()
	cef.Shutdown()


def check_versions():
	ver = cef.GetVersion()
	print("[tutorial.py] CEF Python {ver}".format(ver=ver["version"]))
	print("[tutorial.py] Chromium {ver}".format(ver=ver["chrome_version"]))
	print("[tutorial.py] CEF {ver}".format(ver=ver["cef_version"]))
	print("[tutorial.py] Python {ver} {arch}".format(
		ver=platform.python_version(),
		arch=platform.architecture()[0]))
	assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


if __name__ == '__main__':
	main()
