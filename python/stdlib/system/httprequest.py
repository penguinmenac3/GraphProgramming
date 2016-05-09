try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] HTTP Request", "system.httprequest", {"host": "localhost", "port":80, "method":"get"},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Execute an http request on a host.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        # TODO execute HTTP request
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
