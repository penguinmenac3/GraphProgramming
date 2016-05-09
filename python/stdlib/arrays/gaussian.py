try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
from math import pi, sqrt, exp


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Gaussian Generator", "arrays.gaussian", {"range": 100, "sigma":1},
                                   {},
                                   {"result": "Array"},
                                   "Executes the argument function as python code.", verbose, True, False)
        self.args = args

    def tick(self, value):
        n = self.args["range"]
        sigma = self.args["sigma"]

        r = range(-int(n / 2), int(n / 2) + 1)
        result = [1 / (sigma * sqrt(2 * pi)) * exp(-float(x) ** 2 / (2 * sigma ** 2)) for x in r]

        return {"result": result}
