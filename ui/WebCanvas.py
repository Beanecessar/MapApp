from kivy.garden.cefpython import CefBrowser
import osmnx as ox

class WebCanvas(CefBrowser):
	def __init__(self):
		super().__init__(start_url='http://www.baidu.com')

	def drawRoutes(self, graph, routes, colors):
		fmap = None
		for i in range(len(routes)):
			fmap = ox.plot_route_folium(graph, routes[i], route_map=fmap, route_color=colors[i%len(colors)]+"AA")
		fmap.save("map.html")
		# Display html
		self.load("map.html")

	def drawRoute(self, graph, route, color):
		fmap = ox.plot_route_folium(graph, route, route_color=color)
		fmap.save("map.html")
		# Display html
		self.load("map.html")
