import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Gray to BGR", "extlib.computervision.gray2bgr",
                                   "",
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Convert Gray image to BGR image.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return {"result": img}
