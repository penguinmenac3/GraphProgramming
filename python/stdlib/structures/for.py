try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("For", "stdlib.structures.for", {"n": 1000},
                                   {"trigger": "Object"},
                                   {"loop": "Object", "done": "Object"},
                                   "Do n times.", verbose, loopback="trigger")
        self.args = args
        self.it = 0

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        loop = value["trigger"] if self.it < self.args["n"] else None
        done = value["trigger"] if self.it >= self.args["n"] else None
        self.it = self.it + 1
        
        if tag:
            return {"loop": loop, "done": done, "tags":{"loop":tag, "done":tag}}
        else:
            return {"loop": loop, "done": done}
