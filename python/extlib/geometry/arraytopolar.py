try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import math


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Array 2 Polar", "geometry.arraytopolar", {"total_degree": 270, "center": 0},
                                   {"val": "Array"},
                                   {"result": "PointArray"},
                                   "Transpose points.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        val = value["val"]

        result = []
        start = math.radians(self.args["total_degree"]/2 + self.args["center"])
        step_size = math.radians(self.args["total_degree"]*1.0/len(val))

        for i in range(len(val)):
            result.append([start - step_size * i, val[i]])

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
