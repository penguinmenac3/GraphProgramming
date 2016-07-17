try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Barrier", "stdlib.structures.barrier", {},
                                   {"trigger": "Object", "val": "Object"},
                                   {"trigger": "Object", "val": "Object"},
                                   "Only pass if both are there.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        trigger = value["trigger"]
        val = value["val"]
        
        if tag:
            return {"trigger": trigger, "val":val, "tags":{"trigger":tag, "val":tag}}
        else:
            return {"trigger": trigger, "val":val}
