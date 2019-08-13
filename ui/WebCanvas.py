from kivy.garden.cefpython import CefBrowser

class WebCanvas(CefBrowser):
	def __init__():
		super().__init__(start_url='http://www.baidu.com')

	def drawRoutes(self, routes, color):
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