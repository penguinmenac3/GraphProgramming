try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("HTTP Output", "system.httpoutput", {},
                                   {"val": "String"},
                                   {},
                                   "Output value to http connection.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        # TODO output to tag connection and close connection.
         
        return {}
