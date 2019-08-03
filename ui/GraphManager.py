from ui.GraphCanvas import GraphCanvas

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class GraphManager(object):
	def __init__(self):
		self.canvas = GraphCanvas()

	def drawRoute(frm, to):
		routes = self.canvas.calculateRoute(frm, to)
		if routes:
			self.canvas.drawRoutes(routes, 'red')