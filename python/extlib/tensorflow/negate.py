try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Negate", "extlib.tensorflow.negate", {"code": 'result = value["val"]'},
                                   {"val": "Tensor"},
                                   {"result": "Tensor"},
                                   "Negates a value (-val)", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = -value["val"]
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
