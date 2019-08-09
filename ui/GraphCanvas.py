import osmnx as ox
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from matplotlib.figure import Figure

def TouchPairID(touch1, touch2):
	if touch1.uid < touch2.uid:
		return float("{}.{}".format(touch1.uid, touch2.uid))
	else:
		return float("{}.{}".format(touch2.uid, touch1.uid))

class GraphCanvas(FigureCanvasKivyAgg):
	def __init__(self):
		super().__init__(Figure())
		self.touches = {} # manage multitouch
		self.touchCenter = [0, 0]
		self.touchDistMap = {}
		self.zoomCoeff = 1
		#try:
		#	with open("graph.data", "rb") as f:
		#		self.G = pickle.load(f)
		#except IOError:
		#	self.G = ox.graph_from_place('Modena, Italy', infrastructure='way["power"~"line"]')
		#	with open("graph.data", "wb") as f:
		#		pickle.dump(self.G, f)
		#self.figure, self.ax = ox.plot_graph(self.G, show=False, close=True)

	def refrashRect(self):
		"""
		Every time redraw the canvas, the viewport changes.
		Don't know how to deal with it.
		Use some ticky to refrash canvas.
		"""
		if Window.height <= 720:
			Window.size = (480, 721)
		elif Window.height >= 720:
			Window.size = (480, 719)

	def drawRoute(self, graph, route, color):
		"""
		"""
		self.figure, self.ax = ox.plot_graph_route(graph, route, show=False, close=True, route_color=color)
		self.draw()
		self.refrashRect()

	def drawRoutes(self, graph, routes, colors):
		fmap = None
		colors = ["#FF4040", "#FF7F24", "#FFA500", "#FFFF00", "#9ACD32", "#00FF00", "#7FFFD4", "#00CED1", "#00BFFF"]
		for i in range(len(routes)):
			fmap = ox.plot_route_folium(graph, routes[i], route_map=fmap, route_color=colors[i%len(colors)]+"AA")
		fmap.save("map.html")
		self.figure, self.ax = ox.plot_graph_routes(graph, routes, show=False, close=True, route_color=colors[0])
		self.draw()
		self.refrashRect()

	def updateDistMap(self, touch):
		for t in self.touches.values():
			if t.uid != touch.uid:
				self.touchDistMap[TouchPairID(touch,t)] = touch.distance(t)

	def updateTouchCenter(self):
		if len(self.touches) <= 0:
			return 0, 0
		dx = 0
		dy = 0
		for t in self.touches.values():
			dx += t.x
			dy += t.y
		self.touchCenter = [dx / len(self.touches), dy / len(self.touches)]

	def calAvgDist(self, touch):
		if len(self.touches) <= 0:
			return 0
		totalDist = 0
		for t in self.touches.values():
			if t.uid != touch.uid:
				totalDist += self.touchDistMap[TouchPairID(touch,t)]
		return totalDist / len(self.touches)

	def popDistMap(self, touch):
		for t in self.touches.values():
			if t.uid != touch.uid:
				self.touchDistMap.pop(TouchPairID(touch,t), None)

	def zoomGraph(self, scale):
		"""
		zoom graph
		todo: init self xlim for graph
		"""
		print("GraphCanvas: zoom in: {}".format(scale))
		scalePer = scale/self.width
		xmin, xmax = self.ax.get_xlim()
		self.ax.set(xlim=((xmin+xmax)/2-(xmax-xmin)*(1+scalePer)/2, (xmin+xmax)/2+(xmax-xmin)*(1+scalePer)/2))
		self.draw_idle()

	def moveGraph(self, x, y):
		print("GraphCanvas: move: {}, {}".format(x, y))
		xPer = x/self.width
		xmin, xmax = self.ax.get_xlim()
		xmove = (xmax-xmin)*xPer
		self.ax.set(xlim=(xmin-xmove, xmax-xmove))
		yPer = y/self.height
		ymin, ymax = self.ax.get_ylim()
		ymove = (ymax-ymin)*yPer
		self.ax.set(ylim=(ymin-ymove, ymax-ymove))
		self.draw_idle()

	def on_touch_down(self, touch):
		self.touches[touch.uid] = touch
		self.updateTouchCenter()
		self.updateDistMap(touch)
		if self.collide_point(*touch.pos):
			print("GraphCanvas: on_touch_down at position: {}, {}".format(*touch.pos))
		super().on_touch_down(touch)

	def on_touch_move(self, touch):
		# zoom
		lastDist = self.calAvgDist(touch)
		self.updateDistMap(touch)
		nowDist = self.calAvgDist(touch)
		if len(self.touches) > 1:
			self.zoomGraph(lastDist - nowDist)	
		elif self.collide_point(*touch.pos):
			px, py = self.touchCenter
			self.updateTouchCenter()
			x, y = self.touchCenter
			self.moveGraph(x-px, y-py)
		super().on_touch_move(touch)

	def on_touch_up(self, touch):
		self.touches.pop(touch.uid, None)
		self.popDistMap(touch)
		if self.collide_point(*touch.pos):
			print("GraphCanvas: on_touch_up at position: {}, {}".format(*touch.pos))
		super().on_touch_up(touch)
		