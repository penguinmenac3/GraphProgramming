try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import math


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Polar 2 Euler", "geometry.polartoeuler", {},
                                   {"val": "PointArray"},
                                   {"result": "PointArray"},
                                   "Convert display style.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        val = value["val"]

        result = []
        for p in val:
            result.append([math.cos(p[0]) * p[1], math.sin(p[0]) * p[1]])

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
