from kivy.garden.cefpython import CefBrowser

class WebCanvas(CefBrowser):
	def __init__(self):
		super().__init__(start_url='http://www.baidu.com')