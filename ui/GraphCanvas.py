import osmnx as ox
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

def TouchPairID(touch1, touch2):
	if touch1.uid < touch2.uid:
		return float("{}.{}".format(touch1.uid, touch2.uid))
	else:
		return float("{}.{}".format(touch2.uid, touch1.uid))

class GraphCanvas(FigureCanvasKivyAgg):
	def __init__(self):
		self.touches = {} # manage multitouch
		self.touchCenter = [0, 0]
		self.touchDistMap = {}
		self.zoomCoeff = 1
		graph = ox.graph_from_place('Modena, Italy', infrastructure='way["power"~"line"]')
		fig, ax = ox.plot_graph(graph, show=False, close=True)
		super().__init__(fig)

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

	def zoomInGraph(self, movement):
		print("GraphCanvas: zoom in: {}".format(movement))
		

	def zoomOutGraph(self, movement):
		print("GraphCanvas: zoom out: {}".format(movement))
		

	def moveGraph(self, x, y):
		print("GraphCanvas: move: {}, {}".format(x, y))
		

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
		if lastDist < nowDist:
			self.zoomOut(nowDist - lastDist)
		if nowDist < lastDist:
			self.zoomIn(lastDist - nowDist)
			
		if self.collide_point(*touch.pos):
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