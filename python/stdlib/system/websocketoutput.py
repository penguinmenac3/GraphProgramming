try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] WebSocket", "stdlib.system.websocketoutput", {},
                                   {"val": "Object"},
                                   {},
                                   "Output on a websocket.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        # ToDo write websocket code
        
        return {}
