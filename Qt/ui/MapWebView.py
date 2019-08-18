from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import osmnx as ox
import os

TEMP_PATH = os.getenv('LOCALAPPDATA')+"\\MapQt\\"
TEMP_PATH = TEMP_PATH.replace("\\", "/")

if not os.path.isdir(TEMP_PATH):
	os.makedirs(TEMP_PATH)
print(TEMP_PATH)

class MapWebView(QWebEngineView):
	def __init__(self, parent=None):
		super().__init__(parent)
		if os.path.isfile(TEMP_PATH+"map.html"):
			#self.load(QUrl("file:///"+TEMP_PATH+"map.html"))
			self.load(QUrl.fromLocalFile(TEMP_PATH+"map.html"))

	def drawRoute(self, graph, route, color):
		fmap = ox.plot_route_folium(graph, route, route_color=color)
		fmap.save(TEMP_PATH+"map.html")
		#self.load(QUrl("file:///"+TEMP_PATH+"map.html"))
		self.load(QUrl.fromLocalFile(TEMP_PATH+"map.html"))

	def drawRoutes(self, graph, routes, colors):
		fmap = None
		for i in range(len(routes)):
			fmap = ox.plot_route_folium(graph, routes[i], route_map=fmap, route_color=colors[i%len(colors)]+"AA")
		fmap.save(TEMP_PATH+"map.html")
		#self.load(QUrl("file:///"+TEMP_PATH+"map.html"))
		self.load(QUrl.fromLocalFile(TEMP_PATH+"map.html"))
