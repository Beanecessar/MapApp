import osmnx as ox
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.figure import Figure
import pickle
import networkx as nx

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
		self.highwayWeight = {
			0:{'motorway':1,'trunk':0.7,'primary':0.4,'secondary':0,'tertiary':-0.4,'unclassified':-0.7,'residential':-1},
			1:{'motorway':-1,'trunk':-0.7,'primary':-0.4,'secondary':0,'tertiary':0.4,'unclassified':0.7,'residential':1},
			2:{'motorway':1,'trunk':0,'primary':-0.5,'secondary':-1,'tertiary':-0.5,'unclassified':0,'residential':1},
			3:{'motorway':0.5,'trunk':0,'primary':-1,'secondary':-0.8,'tertiary':-0.6,'unclassified':0,'residential':0.5},
			4:{'motorway':1,'trunk':0.5,'primary':-0.3,'secondary':-0.5,'tertiary':-1,'unclassified':-1,'residential':0}
		}
		self.maxspeedWeight = {0:0.02, 1:-0.02}
		try:
			with open("graph.data", "rb") as f:
				self.G = pickle.load(f)
		except IOError:
			self.G = ox.graph_from_place('Modena, Italy', infrastructure='way["power"~"line"]')
			with open("graph.data", "wb") as f:
				pickle.dump(self.G, f)
		self.figure, self.ax = ox.plot_graph(self.G, show=False, close=True)

	def calculateWeight(self):
		weigetDict = {}
		for i in range(0,5):
			for j in range(0,2):
				for edge in self.G.edges():
					u, v = edge
					d = ox.get_route_edge_attributes(self.G,[u,v],attribute = None,minimize_key ='length',retrieve_default = None)
					length  = d[0]['length']
					a = d[0]
					if 'maxspeed' not in a:
						d[0]['maxspeed'] = '50 mph'
					ret  = re.findall(r'[0-9]+\.?[0-9]*',d[0]['maxspeed'])
					if len(ret) == 0:
						maxspeed = 50
					else:
						maxspeed = float(ret[0])     
					if 'highway' not in a:
						d[0]['highway'] = 'unknown'
					if d[0]['highway'] in highwayWeight[i]:
						highway = highwayWeight[i][d[0]['highway']]
					else:
						highway = 0
					maxspeed = maxspeedWeight[j]*maxspeed_num
					weigetDict[(u, v, 0)] =  length*(1 + maxspeed + highway)
				nx.set_edge_attributes(G, weigetDict, 'type%d'%(j*5+i))

	def calculateRoutes(self,frm, to):
		if isinstance(frm, tuple) and isinstance(to, tuple) :
			fromNode = ox.get_nearest_node(self.G, frm)
			print("GraphCanvas: From nearest node {}.".format(fromNode))
			toNode = ox.get_nearest_node(self.G, to)
			print("GraphCanvas: To nearest node {}.".format(toNode))
			routes = []
			for i in range(0, 9):
				routes.append(nx.shortest_path(self.G, fromNode, toNode, weight='type%d'%(i)))
			return routes

	def drawRoutes(self, routes, color):
		"""
		"""
		self.figure, self.ax = ox.plot_graph_routes(self.G, routes, show=False, close=True, route_color=color)
		self.draw_idle()

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
		
	def userBehavior(self,type_num):
		if typeNum <= 4:
			highwayNum = typyNum
			maxspeedNum = 0
		else:
			highwayNum = typyNum%5
			maxspeedNum = 1
		with open('data.csv','a+', newline='') as f:
			csv_write = csv.writer(f)
			line = []
			for k, v in highwayWeight[highwayNum].items():
				line.append(v)
			line.append(maxspeedWeight[maxspeedNum])
		sv_write.writerow(line)