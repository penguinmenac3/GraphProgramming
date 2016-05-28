try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import sys


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Track", "geometry.track", {"threshold": 10, "max_length": 0, "forget_after": 0},
                                   {"val": "PointArray"},
                                   {"result": "PolygonArray"},
                                   "Track points.", verbose)
        self.args = args
        self.tracks = []
        self.entry_age_queue = []
        self.tresh2 = 100
        self.max_length = 0
        self.forget_after = 20
        if "threshold" in self.args:
            self.tresh2 = self.args["threshold"] * self.args["threshold"]
        if "max_length" in self.args:
            self.max_length = self.args["max_length"]
        if "forget_after" in self.args:
            self.forget_after = self.args["forget_after"]

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        val = value["val"]
        
        if len(val) == 0:
            result = self.tracks
            if tag:
                return {"result": result, "tags": {"result": tag}}
            else:
                return {"result": result}
        if not isinstance(val[0], list):
          val = [val]
        
        todelete = []
        for x in range(len(self.entry_age_queue)):
            if self.entry_age_queue[x] > self.forget_after:
                todelete.append(x)
            self.entry_age_queue[x] = self.entry_age_queue[x] + 1
        
        offset = 0
        for i in range(len(todelete)):
            x = i - offset
            del self.entry_age_queue[x]
            del self.tracks[x]
            offset = offset + 1
        
        for p in val:
            match = None
            index = 0
            for i in range(len(self.tracks)):
                t = self.tracks[i]
                x = t[-1][0]
                y = t[-1][1]
                dx = x - p[0]
                dy = y - p[1]
                if len(t) > 0 and dx*dx + dy*dy < self.tresh2:
                    match = t
                    index = i
            if match:
                match.append(p)
                self.entry_age_queue[index] = 0
                if self.max_length > 0 and len(match) > self.max_length:
                  match.pop(0)
            else:
                new_list = [p]
                self.entry_age_queue.append(0)
                self.tracks.append(new_list)

        result = self.tracks

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
