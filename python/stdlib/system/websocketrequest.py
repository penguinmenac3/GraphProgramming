try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] WebSocket", "system.websocketrequest", {},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Request on a websocket.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        # ToDo write websocket code
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
