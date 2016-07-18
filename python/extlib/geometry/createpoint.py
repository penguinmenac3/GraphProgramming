try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Create Point", "extlib.geometry.createpoint", {},
                                   {"x": "Number", "y": "Number"},
                                   {"point": "Point"},
                                   "Create a point from x and y.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "x" in value["tags"]:
            tag = value["tags"]["x"]
        
        result = [value["x"], value["y"]]
        
        if tag:
            return {"point": result, "tags":{"point":tag}}
        else:
            return {"point": result}
