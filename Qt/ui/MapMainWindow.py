from PyQt5.QtWidgets import QMainWindow, QMessageBox
from geopy.geocoders import Nominatim
from ui.MapMainWindowUI import Ui_MapMainWindow
from ui.MapWebView import MapWebView
from logic.MapManager import MapManager
from logic.LocalInfo import LocalInfo
import math

class MapMainWindow(QMainWindow, Ui_MapMainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.localInfo = LocalInfo()
		self.countryLabel.setText("Country: {}".format(self.localInfo.countryName))
		self.cityLabel.setText("City: {}".format(self.localInfo.cityName))
		self.latitudeLabel.setText("Latitude: {}".format(self.localInfo.latitude))
		self.longitudeLabel.setText("Longitude: {}".format(self.localInfo.longitude))
		self.selectedRoute = None
		self.webView = MapWebView(self.displayArea)
		self.displayArea.layout().addWidget(self.webView)
		self.mapManager = MapManager(self.webView)
		self.routeArea.setVisible(False)
		self.backArea.setVisible(False)
		self.progressBar.setVisible(False)
		self._connect()

	def _connect(self):
		self.cfmPlaceBtn.clicked.connect(self.onConfirmPlace)
		for i in range(10):
			getattr(self, "route"+str(i)).clicked.connect(lambda *arg,btn=getattr(self, "route"+str(i)): self.onPreviewRoute(btn))
		self.allroute.clicked.connect(self.mapManager.drawRoutes)
		self.cfmRouteBtn.clicked.connect(self.onConfirmRoute)
		self.cclRouteBtn.clicked.connect(self.onCancelRoute)
		self.backBtn.clicked.connect(self.onBackClicked)

	def onConfirmPlace(self):
		oriPlace = self.originInput.text()
		destPlace = self.destInput.text()
		if oriPlace == "" or destPlace == "":
			return

		self.progressBar.setVisible(True)
		self.progressBar.setValue(0)
		geolocator = Nominatim()
		tryCount = 10
		print("Start encode the input place.")
		while tryCount > 0:
			try:
				locations = geolocator.geocode(oriPlace, exactly_one=False)
				if locations is None or locations == []:
					QMessageBox.information(self, "Error", "Invaild input place. Please check spelling.")
					self.progressBar.setVisible(False)
					return
				locations.sort(key = lambda elem: math.pow((elem.latitude - self.localInfo.latitude), 2) + math.pow((elem.longitude - self.localInfo.longitude), 2))
				orix = locations[0].latitude
				oriy = locations[0].longitude
		
				locations = geolocator.geocode(destPlace, exactly_one=False)
				if locations is None or locations == []:
					QMessageBox.information(self, "Error", "Invaild input place. Please check spelling.")
					self.progressBar.setVisible(False)
					return
				locations.sort(key = lambda elem: math.pow((elem.latitude - self.localInfo.latitude), 2) + math.pow((elem.longitude - self.localInfo.longitude), 2))
				desx = locations[0].latitude
				desy = locations[0].longitude
			except:
				tryCount -= 1
				self.progressBar.setValue(30 - tryCount*3)
			else:
				self.progressBar.setValue(30)
				print("Encode the input place over.")
				print("Start calculate routes.")
				if (desx - orix)*(desx - orix) + (desy - oriy)*(desy - oriy) > 4:
					QMessageBox.critical(self, "Error", "Too far from origin to destination. From: {} To: {}".format((orix,oriy),(desx,desy)))
				routes = self.mapManager.drawRouteByPos((orix,oriy),(desx,desy),self.progressBar)
				self.progressBar.setValue(90)
				print("Calculate routes over.")
				if len(routes) == 0:
					QMessageBox.critical(self, "Error", "Fail to find valid path.")
					self.progressBar.setVisible(False)
					return
				self.buildRouteArea(routes)
				self.progressBar.setValue(100)
				self.originInput.clear()
				self.destInput.clear()
				self.placeArea.setVisible(False)
				self.routeArea.setVisible(True)
				self.progressBar.setVisible(False)
				return
		QMessageBox.information(self, "Error", "Fail to locate the input place due to networking problems. Please retry.")

	def onPreviewRoute(self, btn):
		print("onPreviewRoute", btn.routeNum)
		self.selectedRoute = btn.routeNum
		self.mapManager.drawRouteByID(btn.routeNum)

	def onConfirmRoute(self):
		print("onPreviewRoute", self.selectedRoute)
		if self.selectedRoute is not None:
			self.mapManager.routeSelected(self.selectedRoute)
			self.backArea.setVisible(True)
			self.routeArea.setVisible(False)

	def onCancelRoute(self):
		self.selectedRoute = None
		self.placeArea.setVisible(True)
		self.routeArea.setVisible(False)

	def onBackClicked(self):
		self.placeArea.setVisible(True)
		self.backArea.setVisible(False)

	def buildRouteArea(self, routes):
		count = 0
		for i in range(len(routes)):
			isUnique = True
			for j in range(i):
				print("Compare routes {} with routes {}.".format(i, j))
				if routes[i] == routes[j]:
					isUnique = False
					print("Equal.")
				else:
					print("Not equal.")
			if isUnique:
				routeLen = self.mapManager.getRouteLength(routes[i])
				getattr(self, "route"+str(count)).routeNum = count
				getattr(self, "route"+str(i)).setVisible(True)
				getattr(self, "route"+str(i)).setText("Route{}({}km)".format(count, round(routeLen/1000.0, 2)))
				count += 1
		for i in range(count, 10):
			getattr(self, "route"+str(i)).setVisible(False)
