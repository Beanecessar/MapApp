import osmnx as ox
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

class GraphManager(object):
	def __init__(self):
		graph = ox.graph_from_place('Modena, Italy')
		fig, ax = ox.plot_graph(graph, show=False, close=True)
		self.canvas = FigureCanvasKivyAgg(fig)