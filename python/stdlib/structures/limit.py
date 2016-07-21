try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import time

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("limit", "stdlib.structures.limit", {"Hz":1.0},
                                   {"in": "Object"},
                                   {"out": "Object"},
                                   "Only pass once per timelimit.", verbose)
        self.args = args
        self.t = time.time()

    def tick(self, value):
        tag = None
        if "tags" in value and "a" in value["tags"]:
            tag = value["tags"]["a"]
        
        a = value["in"]
        dt = time.time() - self.t
        if dt > 1.0 / self.args["Hz"]:
            self.t = time.time()
        else:
            a = None
        
        if tag:
            return {"out": a, "tags":{"out":tag}}
        else:
            return {"out": a}
