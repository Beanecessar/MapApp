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
		fromInput.add_widget(Label(text="Latitude"))
		self.fromXInput = FloatInput(text="39.90")
		fromInput.add_widget(self.fromXInput)
		fromInput.add_widget(Label(text="Longitude"))
		self.fromYInput = FloatInput(text="116.40")
		fromInput.add_widget(self.fromYInput)
		self.inputLayout.add_widget(fromInput)
		self.inputLayout.add_widget(Label(text="To", height=20))
			# To
		toInput = BoxLayout(size_hint=(1, None), height=30)
		toInput.add_widget(Label(text="Latitude"))
		self.toXInput = FloatInput(text="39.92")
		toInput.add_widget(self.toXInput)
		toInput.add_widget(Label(text="Longitude"))
		self.toYInput = FloatInput(text="116.42")
		toInput.add_widget(self.toYInput)
		self.inputLayout.add_widget(toInput)
		self.add_widget(self.inputLayout)

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
		self.previewNo = -1
		self.routeBtnList = []
		if routeNum == 0:
			return
		self.remove_widget(self.inputLayout)
		self.remove_widget(self.confirmBtn)
		for no in range(routeNum):
			routeBtn = Button(text=str(no), size_hint=(None, None), width=30)
			routeBtn.bind(on_press=self.previewRoute)
			self.routeBtnList.append(routeBtn)
			self.add_widget(routeBtn)
		self.add_widget(self.selectBtn)

	def previewRoute(self, instance):
		value = int(instance.text)
		self.previewNo = value
		self.parent.graphManager.drawRouteByID(value)

	def routeSelected(self, instance):
		value = self.previewNo
		self.parent.graphManager.routeSelected(value)
		self.remove_widget(self.routeSpiner)
		self.remove_widget(self.selectBtn)
		self.add_widget(self.backBtn)

	def clearRoute(self, instance):
		self.remove_widget(self.backBtn)
		self.add_widget(self.inputLayout)
		self.add_widget(self.confirmBtn)
