try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Sync", "stdlib.structures.sync", {},
                                   {"a": "Object", "b": "Object"},
                                   {"a": "Object", "b": "Object"},
                                   "Only pass if both are there.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "a" in value["tags"]:
            tag = value["tags"]["a"]
        
        a = value["a"]
        b = value["b"]
        
        if tag:
            return {"a": a, "b":b, "tags":{"a":tag, "b":tag}}
        else:
            return {"a": a, "b":b}
