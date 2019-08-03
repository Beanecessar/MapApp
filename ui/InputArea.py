from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from ui.FloatInput import FloatInput
from kivy.uix.spinner import Spinner

class InputArea(BoxLayout):
	def __init__(self):
		super().__init__(size_hint=(1, None), height=80)

		inputLayout = BoxLayout(orientation="vertical")
		inputLayout.add_widget(Label(text="From", height=20))
		# From
		fromInput = BoxLayout(size_hint=(1, None), height=20)
		fromInput.add_widget(Label(text="X"))
		self.fromXInput = FloatInput(text="0.00000")
		fromInput.add_widget(self.fromXInput)
		fromInput.add_widget(Label(text="Y"))
		self.fromYInput = FloatInput(text="0.00000")
		fromInput.add_widget(self.fromYInput)
		inputLayout.add_widget(fromInput)
		inputLayout.add_widget(Label(text="To", height=20))
		# To
		toInput = BoxLayout(size_hint=(1, None), height=20)
		toInput.add_widget(Label(text="X"))
		self.toXInput = FloatInput(text="0.00000")
		toInput.add_widget(self.toXInput)
		toInput.add_widget(Label(text="Y"))
		self.toYInput = FloatInput(text="0.00000")
		toInput.add_widget(self.toYInput)
		inputLayout.add_widget(toInput)
		self.add_widget(inputLayout)

		confirmBtn = Button(text="Confirm")
		confirmBtn.bind(on_press=self.fromToConfirm)
		self.add_widget(confirmBtn)

	def fromToConfirm(self, instance):
		fx = float(self.fromXInput.text)
		fy = float(self.fromYInput.text)
		tx = float(self.toXInput.text)
		ty = float(self.toYInput.text)
		self.parent.graphManager.drawRoute((fx,fy),(tx,ty))