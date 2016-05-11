import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Resize", "computervision.resize",
                                   {"width": 320, "height": 240},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Resize an image.", verbose)
        self.args = args

    def tick(self, value):
        width = self.args["width"]
        height = self.args["height"]
        img = value["img"]
        img = cv2.resize(img, (width, height), 0, 0, cv2.INTER_CUBIC)
        return {"result": img}
