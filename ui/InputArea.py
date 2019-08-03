from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from ui.FloatInput import FloatInput
from kivy.uix.spinner import Spinner

class InputArea(BoxLayout):
	def __init__(self):
		super().__init__(size_hint=(1, None), height=100)
		# Input layout
		self.inputLayout = BoxLayout(orientation="vertical")
		self.inputLayout.add_widget(Label(text="From", height=20))
			# From
		fromInput = BoxLayout(size_hint=(1, None), height=30)
		fromInput.add_widget(Label(text="X"))
		self.fromXInput = FloatInput(text="0.00000")
		fromInput.add_widget(self.fromXInput)
		fromInput.add_widget(Label(text="Y"))
		self.fromYInput = FloatInput(text="0.00000")
		fromInput.add_widget(self.fromYInput)
		self.inputLayout.add_widget(fromInput)
		self.inputLayout.add_widget(Label(text="To", height=20))
			# To
		toInput = BoxLayout(size_hint=(1, None), height=30)
		toInput.add_widget(Label(text="X"))
		self.toXInput = FloatInput(text="0.00000")
		toInput.add_widget(self.toXInput)
		toInput.add_widget(Label(text="Y"))
		self.toYInput = FloatInput(text="0.00000")
		toInput.add_widget(self.toYInput)
		self.inputLayout.add_widget(toInput)
		self.add_widget(self.inputLayout)

		self.routeSpiner = Spinner(text="None")
		self.routeSpiner.bind(text=self.previewRoute)
		# self.add_widget(self.routeSpiner)

		# Confirm button
		self.confirmBtn = Button(text="Confirm", size_hint=(None, None), width=80)
		self.confirmBtn.bind(on_press=self.fromToConfirmed)
		self.add_widget(self.confirmBtn)

		# Select button
		self.selectBtn = Button(text="Confirm", size_hint=(None, None), width=80)
		self.selectBtn.bind(on_press=self.routeSelected)
		# self.add_widget(self.selectBtn)

		self.backBtn = Button(text="Back", size_hint=(None, None), width=80)
		self.backBtn.bind(on_press=self.clearRoute)

	def fromToConfirmed(self, instance):
		fx = float(self.fromXInput.text)
		fy = float(self.fromYInput.text)
		tx = float(self.toXInput.text)
		ty = float(self.toYInput.text)
		routeNum = self.parent.graphManager.drawRouteByPos((fx,fy),(tx,ty))
		if routeNum == 0:
			return
		self.routeSpiner.text = "All"
		self.routeSpiner.values = ["All"] + [str(x) for x in range(0, routeNum)]
		self.remove_widget(self.inputLayout)
		self.remove_widget(self.confirmBtn)
		self.add_widget(self.routeSpiner)
		self.add_widget(self.selectBtn)

	def previewRoute(self, instance, value):
		if value in ["", "None", "All"]:
			return
		value = int(value)
		self.parent.graphManager.drawRouteByID(value)

	def routeSelected(self, instance):
		value = self.routeSpiner.text
		if value in ["", "None"]:
			return
		if value == "All":
			self.parent.graphManager.drawRoute()
			return
		value = int(value)
		self.parent.graphManager.routeSelected(value)
		self.remove_widget(self.routeSpiner)
		self.remove_widget(self.selectBtn)
		self.add_widget(self.backBtn)

	def clearRoute(self, instance):
		self.remove_widget(self.backBtn)
		self.add_widget(self.inputLayout)
		self.add_widget(self.confirmBtn)
