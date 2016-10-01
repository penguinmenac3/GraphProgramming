try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
from math import pi, sqrt, exp

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("To Gaussian", "stdlib.arrays.togaussian", {"range": 80},
                                   {"mu": "Number", "sigma": "Number"},
                                   {"distribution": "Array"},
                                   "Create a gaussian.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "mu" in value["tags"]:
            tag = value["tags"]["mu"]
        
        n = self.args["range"]
        sigma = value["sigma"]
        mu = value["mu"]

        r = range(0, n)
        result = [1 / (sigma * sqrt(2 * pi)) * exp(-float(x-mu) ** 2 / (2 * sigma ** 2)) for x in r]
        
        if tag:
            return {"distribution": result, "tags":{"distribution":tag}}
        else:
            return {"distribution": result}
