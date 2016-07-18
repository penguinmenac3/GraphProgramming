try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Accumulate", "extlib.geometry.accumulate", {},
                                   {"p": "Point"},
                                   {"acc": "PointArray"},
                                   "Just add the points to Pointarray", verbose)
        self.args = args
        self.accumulator = []

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "p" in value["tags"]:
            tag = value["tags"]["p"]
        
        self.accumulator.append(value["p"])
        
        if tag:
            return {"acc": self.accumulator, "tags":{"acc":tag}}
        else:
            return {"acc": self.accumulator}
