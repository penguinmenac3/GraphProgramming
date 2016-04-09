try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Function", "default.function", {"code": 'result = value["val"]'},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Executes the argument as pyton code.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        exec(self.args["code"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
