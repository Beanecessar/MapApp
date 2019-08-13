from kivy.app import App
from ui.MainLayout import MainLayout
from kivy.config import Config

class TestApp(App):
	title = "App Name"
	def __init__(self):
		super().__init__()

	def build(self):
		self.mainLayout = MainLayout()
		return self.mainLayout

if __name__ == "__main__":
	# Config.set('kivy', 'keyboard_mode', 'systemandmulti')
	TestApp().run()