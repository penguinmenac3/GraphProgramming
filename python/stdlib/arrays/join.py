try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Join", "stdlib.arrays.join", {},
                                   {"a": "Array", "b": "Array"},
                                   {"result": "Array"},
                                   "Executes the argument as pyton code.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "a" in value["tags"]:
            tag = value["tags"]["a"]
        
        result = []
        for x in value["a"]:
          result.append(x)
        for x in value["b"]:
          result.append(x)
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
