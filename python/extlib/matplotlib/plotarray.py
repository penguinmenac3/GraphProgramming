try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import matplotlib.pyplot as plt


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] Plot Array", "matplotlib.plotarray",
                                   {"ion": True, "title": "Debug", "clear": True, "subplot": 111},
                                   {"data": "Array"},
                                   {},
                                   "Plot an array.", verbose, False, False, True)
        self.args = args
        self.fig = None
        self.ax1 = None

    def tick(self, value):
        if self.args["ion"]:
            plt.ion()

        data = value["data"]
        # TODO more features and more specific stuff.
        self.fig = plt.figure(self.args["title"])
        self.ax1 = self.fig.add_subplot(self.args["subplot"])
        if self.args["clear"]:
            plt.cla()

        self.ax1.plot(data)
        plt.show()
        plt.pause(0.0001)
        return {}
