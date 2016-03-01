try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Fixed Saturisation", "computervision.fixedsaturisation",
                                   127,
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Set the saturisation to a fixed value.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img[:, :, 1] = self.args
        return {"result": img}