from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from ui.FloatInput import FloatInput

class InputArea(BoxLayout):
	def __init__(self):
		super().__init__(orientation="vertical", size_hint=(1, None), height=60)
		self.add_widget(Label(text="Destination"))
		destInput = BoxLayout(size_hint=(1, None), height=30)
		self.add_widget(destInput)

		destInput.add_widget(Label(text="X"))
		destInput.add_widget(FloatInput(text="0.00000"))
		destInput.add_widget(Label(text="Y"))
		destInput.add_widget(FloatInput(text="0.00000"))
