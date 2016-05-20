try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Track", "geometry.track", {"threshold": 10, "max_length": 0},
                                   {"val": "PointArray"},
                                   {"result": "PolygonArray"},
                                   "Track points.", verbose)
        self.args = args
        self.tracks = []
        self.tresh2 = 100
        self.max_length = 0
        if "threshold" in self.args:
            self.tresh2 = self.args["threshold"] * self.args["threshold"]
        if "max_length" in self.args:
            self.max_length = self.args["max_length"]

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        val = value["val"]
        
        if not isinstance(val[0], list):
          val = [val]
        
        for p in val:
            match = None
            for t in self.tracks:
                x = t[-1][0]
                y = t[-1][1]
                dx = x - p[0]
                dy = y - p[1]
                if len(t) > 0 and dx*dx + dy*dy < self.tresh2:
                    match = t
            if match:
                match.append(p)
                if len(match) > self.max_length:
                  match.pop(0)
            else:
                self.tracks.append([p])

        result = self.tracks

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
