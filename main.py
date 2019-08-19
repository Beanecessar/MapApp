from kivy.app import App
from ui.MainLayout import MainLayout


class TestApp(App):
	title = "App Name"
	def __init__(self):
		super().__init__()

	def build(self):
		self.mainLayout = MainLayout()
		return self.mainLayout

if __name__ == "__main__":
	TestApp().run()