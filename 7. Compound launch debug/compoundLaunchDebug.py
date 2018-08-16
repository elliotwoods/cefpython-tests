# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
import base64
import platform
import sys
import os
import threading
import traceback

def main():
	# Use paths relative to this python file
	pythonFileFolder = os.path.dirname(os.path.realpath(__file__))
	os.chdir(pythonFileFolder)

	_, innerFolder = os.path.split(pythonFileFolder)
	
	check_versions()
	sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
	
	settings = {
		"remote_debugging_port": 49155,
	}

	cef.SetGlobalClientCallback("OnAfterCreated", on_after_create)

	cef.Initialize(settings=settings)


	browser = cef.CreateBrowserSync(url='file:///index.html',
									window_title=innerFolder)
	clientHandler = ClientHandler()
	browser.SetClientHandler(clientHandler)

	bindings = cef.JavascriptBindings()
	testObject = TestObject()
	bindings.SetObject("testObject", testObject)
	browser.SetJavascriptBindings(bindings)

	cef.MessageLoop()
	cef.Shutdown()

def on_after_create(browser, **_):
	print("Created")
	pass

class ClientHandler(object):
	def OnLoadingStateChange(self, browser, is_loading, **_):
		print ("Loading : {0}".format(is_loading))
		if not is_loading:
			browser.ExecuteFunction("test_function")
			browser.ExecuteFunction("call_test_object")
	
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

def jsWrap(function):
	'''Wrapper to handle returns and exceptions'''

	def wrappedFunction(callObject, successCallback, exceptionCallback, *args):
		try:
			result = function(args)
			successCallback.Call(result)
		except Exception as exception:
			# Get the traceback info
			exc_tb = sys.exc_info()[2]
			tracebackList = traceback.extract_tb(exc_tb, 5)

			formattedTracebackList = []
			for tracebackEntry in tracebackList:
				formattedTracebackList.append({
					"name" : tracebackEntry.name,
					"filename" : tracebackEntry.filename,
					"lineNumber" : tracebackEntry.lineno,
					"line" : tracebackEntry.line
				})

			formattedException = {
				"type" : type(exception),
				"args" : exception.args,
				"message" : str(exception),
				"traceback" : formattedTracebackList
			}
		
			exceptionCallback.Call(formattedException)

	return wrappedFunction
		

class TestObject(object):
	def test_method(self):
		print("Test method called on Python TestObject")
		return [1, 2, 3, 4]

	def test_method_throws_exception(self):
		raise(Exception("Here's an exception"))

	testMethod = jsWrap(test_method)
	testMethodThrowsException = jsWrap(test_method_throws_exception)

if __name__ == '__main__':
	main()
