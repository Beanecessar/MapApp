from kivy.uix.boxlayout import BoxLayout
from ui.GraphManager import GraphManager
from ui.InputArea import InputArea

class MainLayout(BoxLayout):
	def __init__(self):
		super().__init__(orientation='vertical')
		self.graphManager = GraphManager()
		self.textInput = InputArea()
		self.add_widget(self.graphManager.canvas)
		self.add_widget(self.textInput)