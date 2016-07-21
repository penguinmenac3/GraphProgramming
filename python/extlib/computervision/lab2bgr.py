import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Lab to BGR", "extlib.computervision.lab2bgr",
                                   "",
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Convert Lab image to BGR image.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
        return {"result": img}
