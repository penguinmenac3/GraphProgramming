try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Pass", "stdlib.default.pass", {},
                                   {"in": "Object"},
                                   {"out": "Object"},
                                   "Pass the input to out.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "in" in value["tags"]:
            tag = value["tags"]["in"]
        
        result = value["in"]
        
        if tag:
            return {"out": result, "tags":{"out":tag}}
        else:
            return {"out": result}
