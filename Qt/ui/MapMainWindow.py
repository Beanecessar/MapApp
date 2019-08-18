from PyQt5.QtWidgets import QMainWindow, QMessageBox
from geopy.geocoders import Nominatim
from ui.MapMainWindowUI import Ui_MapMainWindow
from ui.MapWebView import MapWebView
from logic.MapManager import MapManager

class MapMainWindow(QMainWindow, Ui_MapMainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.selectedRoute = None
		self.webView = MapWebView(self.displayArea)
		self.displayArea.layout().addWidget(self.webView)
		self.mapManager = MapManager(self.webView)
		self.routeArea.setVisible(False)
		self.backArea.setVisible(False)
		self._connect()

	def _connect(self):
		self.cfmPlaceBtn.clicked.connect(self.onConfirmPlace)
		for i in range(9):
			getattr(self, "route"+str(i)).clicked.connect(lambda index=i: self.onPreviewRoute)
		self.allroute.clicked.connect(lambda: self.mapManager.drawRoutes)
		self.cfmRouteBtn.clicked.connect(self.onConfirmRoute)
		self.cclRouteBtn.clicked.connect(self.onCancelRoute)
		self.backBtn.clicked.connect(self.onBackClicked)

	def onConfirmPlace(self):
		oriPlace = self.originInput.text()
		destPlace = self.destInput.text()
		if oriPlace == "" or destPlace == "":
			return

		geolocator = Nominatim()
		tryCount = 10
		while tryCount > 0:
			try:
				location = geolocator.geocode(oriPlace)
				orix = location.latitude
				oriy = location.longitude
		
				location = geolocator.geocode(destPlace)
				desx = location.latitude
				desy = location.longitude
			except:
				tryCount -= 1
			else:
				print(orix, oriy, desx, desy)
				routeNum = self.mapManager.drawRouteByPos((orix,oriy),(desx,desy))
				self.buildRouteArea(routeNum)
				self.originInput.clear()
				self.destInput.clear()
				self.placeArea.setVisible(False)
				self.routeArea.setVisible(True)
				self.mapManager.drawRoutes()
				return
		QMessageBox.information(self, "Error", "Fail to locate the input place due to networking problems. Please retry.")

	def onPreviewRoute(self, rid):
		self.selectedRoute = rid
		self.mapManager.drawRouteByID(rid)

	def onConfirmRoute(self):
		if self.selectedRoute:
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

	def buildRouteArea(self, routeNum):
		for i in range(9):
			if i < routeNum:
				getattr(self, "route"+str(i)).setVisible(True)
			else:
				getattr(self, "route"+str(i)).setVisible(False)
