from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from ui.FloatInput import FloatInput

class InputArea(BoxLayout):
	def __init__(self):
		super().__init__(orientation="vertical", size_hint=(1, None), height=60)
		self.add_widget(Label(text="Destination"))
		destInput = BoxLayout(size_hint=(1, None), height=30)
		self.add_widget(destInput)

		destInput.add_widget(Label(text="X"))
		self.destXInput = FloatInput(text="0.00000")
		destInput.add_widget(self.destXInput)
		destInput.add_widget(Label(text="Y"))
		self.destYInput = FloatInput(text="0.00000")
		destInput.add_widget(self.destYInput)
		confirmBtn = Button(text="Confirm")
		confirmBtn.bind(on_press=self.destConfirm)
		destInput.add_widget(confirmBtn)

	def destConfirm(self, instance):
		x = self.destXInput.text
		y = self.destXInput.text
		print("InputArea: destination confirm, pos: {}, {}".format(x, y))