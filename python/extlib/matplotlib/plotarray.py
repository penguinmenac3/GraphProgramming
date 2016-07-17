try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import matplotlib
matplotlib.use("qt4agg")
from matplotlib import pyplot as plt

import time
import sys

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] Plot Array", "extlib.matplotlib.plotarray",
                                   {"ion": True, "title": "Debug", "clear": True, "subplot": 111},
                                   {"data": "Array"},
                                   {},
                                   "Plot an array.", verbose, False, False, True)
        self.args = args
        self.fig = None
        self.ax1 = None

    def tick(self, value):
        #t = time.time()
        #if self.args["ion"]:
            #plt.ion()
            
        data = value["data"]
        # TODO more features and more specific stuff.
        if not self.fig and not self.ax1:
        	self.fig = plt.figure(self.args["title"])
        	self.ax1 = self.fig.add_subplot(self.args["subplot"])
        if self.args["clear"]:
            self.ax1.cla()

        self.ax1.plot(data)
        if not self.args["ion"]:
        	plt.show()
        else:
        	plt.pause(0.0001)
        #elapsed = time.time() - t
        #print(elapsed)
        #sys.stdout.flush()
        return {}
