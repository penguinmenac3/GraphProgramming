try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Fixed Intensity", "computervision.fixedintensity",
                                   127,
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Set the intensity to a fixed value.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img[:, :, 2] = self.args
        return {"result": img}
