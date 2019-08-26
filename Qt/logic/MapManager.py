import osmnx as ox
import csv
import re
import networkx as nx

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class MapManager(object):
	def __init__(self, canvas):
		self.routeColorMap = ["#FF4040", "#FF7F24", "#FFA500", "#FFFF00", "#9ACD32", "#00FF00", "#7FFFD4", "#00CED1", "#00BFFF", "#4F2F4F"]
		self.highwayWeight = {
			0:{'motorway':1,'trunk':0.7,'primary':0.4,'secondary':0,'tertiary':-0.4,'unclassified':-0.7,'residential':-1},
			1:{'motorway':-1,'trunk':-0.7,'primary':-0.4,'secondary':0,'tertiary':0.4,'unclassified':0.7,'residential':1},
			2:{'motorway':1,'trunk':0,'primary':-0.5,'secondary':-1,'tertiary':-0.5,'unclassified':0,'residential':1},
			3:{'motorway':0.5,'trunk':0,'primary':-1,'secondary':-0.8,'tertiary':-0.6,'unclassified':0,'residential':0.5},
			4:{'motorway':1,'trunk':0.5,'primary':-0.3,'secondary':-0.5,'tertiary':-1,'unclassified':-1,'residential':0}
		}
		self.maxspeedWeight = {0:0.02, 1:-0.02}
		try:
			self.wayPreference,self.speedPreference,self.columsLen = self.behavioralLearning()
		except:
			self.columsLen = 0

		self.canvas = canvas
		self.routes = []

	def getRouteLength(self, route):
		return round(sum(ox.get_route_edge_attributes(self.G,route,attribute = 'length',minimize_key ='length',retrieve_default = None)), 3)

	def drawRoutes(self):
		self.canvas.drawRoutes(self.G, self.routes, self.routeColorMap)

	def drawRouteByPos(self, frm, to, progress=None):
		self.routes = self.calculateRoutes(frm, to, progress)
		if len(self.routes) > 0:
			print("MapManager: Find %d routes."%(len(self.routes)))
			self.canvas.drawRoutes(self.G, self.routes, self.routeColorMap)
		return self.routes

	def drawRouteByID(self, rid):
		color = self.routeColorMap[rid%len(self.routeColorMap)]
		print("Draw route {} {}".format(rid, self.routes[rid]))
		self.canvas.drawRoute(self.G, self.routes[rid], color)

	def routeSelected(self, rid):
		print("MapManager: Selected route %d."%(rid))
		self.userBehavior(rid)

	def calculateWeight(self):
		weigetDict = {}
		for i in range(0,5):
			for j in range(0,2):
				for edge in self.G.edges():
					u, v = edge
					d = ox.get_route_edge_attributes(self.G,[u,v],attribute = None,minimize_key ='length',retrieve_default = None)
					length  = d[0]['length']
					a = d[0]
					if 'maxspeed' not in a or not isinstance(a, (str, bytes)):
						a['maxspeed'] = '50 mph'
					ret  = re.findall(r'[0-9]+\.?[0-9]*',a['maxspeed'])
					if len(ret) == 0:
						maxspeedNum = 50
					else:
						maxspeedNum = float(ret[0])
					highway = 0 # default value
					if 'highway' in a:
						if isinstance(a['highway'], list):
							a['highway'] = a['highway'][0]
						if isinstance(a['highway'], str):
							if a['highway'] in self.highwayWeight[i]:
								highway = self.highwayWeight[i][a['highway']]
					maxspeed = self.maxspeedWeight[j]*maxspeedNum
					weight = length*(1 + maxspeed*0.5 + highway*0.5)
					if weight < 0:
						weight = 0
					weigetDict[(u, v, 0)] = weight
				nx.set_edge_attributes(self.G, weigetDict, 'type%d'%(j*5+i))
	
		if self.columsLen > 10:
				for edge in self.G.edges():
					u, v = edge
					d = ox.get_route_edge_attributes(self.G,[u,v],attribute = None,minimize_key ='length',retrieve_default = None)
					length  = d[0]['length']
					a = d[0]
					if 'maxspeed' not in a:
						d[0]['maxspeed'] = '50 mph'
					ret  = re.findall(r'[0-9]+\.?[0-9]*',d[0]['maxspeed'])
					if len(ret) == 0:
						maxspeedNum = 50
					else:
						maxspeedNum = float(ret[0])
					highway = 0 # default value
					if 'highway' in a:
						if isinstance(a['highway'], list):
							a['highway'] = a['highway'][0]
						if isinstance(a['highway'], str):
							if a['highway'] in self.wayPreference:
								highway = self.wayPreference[a['highway']]
					maxspeed = self.speedPreference*maxspeedNum
					weight = length*(1 + maxspeed*0.5 + highway*0.5)
					if weight < 0:
						weight = 0
					weigetDict[(u, v, 0)] = weight
				nx.set_edge_attributes(self.G, weigetDict, 'type10')

	@staticmethod
	def GetBBox(frm, to):
		north = max(frm[0], to[0])+0.001
		south = min(frm[0], to[0])-0.001
		east = max(frm[1], to[1])+0.001
		west = min(frm[1], to[1])-0.001
		return north, south, east, west

	@staticmethod
	def GetCenter(frm, to):
		x = (frm[0] + to[0]) / 2
		y = (frm[1] + to[1]) / 2
		return (x, y)

	def calculateRoutes(self, frm, to, progress=None):
		print("Calculate routes from {} to {}".format(frm, to))
		if isinstance(frm, tuple) and isinstance(to, tuple):
			#center = self.GetCenter(frm, to)
			north, south, east, west = self.GetBBox(frm, to)
			try:
				self.G = ox.graph_from_bbox(north, south, east, west, truncate_by_edge=True)
				#self.G = ox.graph_from_point(center, truncate_by_edge=True)
			except Exception as e:
				print("MapManager: Error when get graph.\n%s"%(str(e)))
				return []
			self.calculateWeight()
			fromNode = ox.get_nearest_node(self.G, frm)
			print("GraphCanvas: From nearest node {}.".format(fromNode))
			toNode = ox.get_nearest_node(self.G, to)
			print("GraphCanvas: To nearest node {}.".format(toNode))
			routes = []
			try:
				for i in range(10):
					if progress:
						progress.setValue(60+i*2)
					routes.append(nx.shortest_path(self.G, fromNode, toNode, weight='type%d'%(i)))
				if self.columsLen >= 10:
					routes.append(nx.shortest_path(self.G, fromNode, toNode, weight='type10'))
				return routes
			except:
				pass
		return []

	def userBehavior(self, typeNum):
		if typeNum == 10:
			with open('data.csv','a+', newline='') as f:
				csv_write = csv.writer(f)
				line = []
				for k, v in self.wayPreference.items():
					line.append(v)
				line.append(self.speedPreference)
				csv_write.writerow(line)
		else:
			if typeNum <= 4:
				highwayNum = typeNum
				maxspeedNum = 0
			else:
				highwayNum = typeNum%5
				maxspeedNum = 1
			with open('data.csv','a+', newline='') as f:
				csv_write = csv.writer(f)
				line = []
				for k, v in self.highwayWeight[highwayNum].items():
					line.append(v)
					line.append(self.maxspeedWeight[maxspeedNum])
				csv_write.writerow(line)

	def behavioralLearning(self):
		with open('data.csv','r') as csvfile:
			reader = csv.reader(csvfile)
			data = [row for row in reader]
			columsLen = len([colums[0] for colums in data])
			wayWeight = {}
			L = []
			for i in range(0,8):
				cols= [col[i] for col in data]
				cols.remove(max(cols))
				cols.remove(min(cols))
				cols = list(map(float, cols))
				avg = np.mean(cols)
				L.append(avg)
		waytype = ['motorway','trunk','primary','secondary','tertiary','unclassified','residential']
		for i in range(0, 7):
			wayWeight[waytype[i]] = L[i]
		speedWeight = L[7]
		return wayWeight,speedWeight,columsLen