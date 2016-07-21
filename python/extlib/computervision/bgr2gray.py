import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("BGR to Gray", "extlib.computervision.bgr2gray",
                                   "",
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Convert BGR image to Gray image.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return {"result": img}
