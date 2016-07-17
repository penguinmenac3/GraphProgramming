try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Crop Image", "extlib.computervision.crop", {"x":0, "y":0, "width":320, "height":240},
                                   {"val": "Image"},
                                   {"result": "Image"},
                                   "Crop the image", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        x = self.args["x"]
        y = self.args["y"]
        w = self.args["width"]
        h = self.args["height"]
        result = value["val"][y:y+h, x:x+w]
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
