from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from geopy.geocoders import Nominatim
#from ui.FloatInput import FloatInput
from kivy.uix.spinner import Spinner

class InputArea(BoxLayout):
	def __init__(self):
		super().__init__(size_hint=(1, None), height=100)
		# Input layout
		self.inputLayout = BoxLayout(orientation="vertical")
			# Origin
		self.inputLayout.add_widget(Label(text="Origin", height=20))
		self.fromPlace = TextInput(text="")
		self.inputLayout.add_widget(self.fromPlace)
			# Destination
		self.inputLayout.add_widget(Label(text="Destination", height=20))
		self.toPlace = TextInput(text="")
		self.inputLayout.add_widget(self.toPlace)
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
		if self.fromPlace.text == "" or self.toPlace.text == "":
			return

		geolocator = Nominatim()

		try:
			location = geolocator.geocode(self.fromPlace.text)
			fx = location.latitude
			fy = location.longitude
		except:
			return

		try:
			location = geolocator.geocode(self.toPlace.text)
			tx = location.latitude
			ty = location.longitude
		except:
			return

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
		for btn in self.routeBtnList:
			self.remove_widget(btn)
		self.remove_widget(self.selectBtn)
		self.add_widget(self.backBtn)

	def clearRoute(self, instance):
		self.remove_widget(self.backBtn)
		self.add_widget(self.inputLayout)
		self.add_widget(self.confirmBtn)
