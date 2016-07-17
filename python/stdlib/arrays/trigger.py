try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import time


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Array trigger", "stdlib.arrays.trigger", {"vals": [0, 1, 2, 3, 4, 5], "time": 1.0},
                                   {},
                                   {"result": "Array"},
                                   "A constant input array.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        return {"result": self.args["vals"]}
