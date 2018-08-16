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
	}

	cef.SetGlobalClientCallback("OnAfterCreated", on_after_create)

	cef.Initialize(settings=settings)

	browser = cef.CreateBrowserSync(url='file:///html/hello_world.html',
									window_title="2. Handlers")
	clientHandler = ClientHandler()
	browser.SetClientHandler(clientHandler)

	cef.MessageLoop()
	cef.Shutdown()

def on_after_create(browser, **_):
	print("Created")
	pass

class ClientHandler(object):
	def OnLoadingStateChange(self, browser, is_loading, **_):
		print ("Loading : {0}".format(is_loading))
	
	def OnConsoleMessage(self, browser, message, **_):
		print ("JS Console Message : {0}".format(message))

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
