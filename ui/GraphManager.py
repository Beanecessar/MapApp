from ui.GraphCanvas import GraphCanvas

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class GraphManager(object):
	def __init__(self):
		self.canvas = GraphCanvas()
		self.routes = []

	def drawRoute(self):
		self.canvas.drawRoutes(self.routes, 'red')

	def drawRouteByPos(self,frm, to):
		self.routes = self.canvas.calculateRoutes(frm, to)
		if len(self.routes) > 0:
			print("GraphManager: Find %d routes."%(len(self.routes)))
			self.canvas.drawRoutes(self.routes, 'red')
		return len(self.routes)

	def drawRouteByID(self, rid):
		self.canvas.drawRoute(self.routes[rid], 'red')

	def routeSelected(self, rid):
		print("GraphManager: Selected route %d."%(rid))
		self.canvas.userBehavior(rid)