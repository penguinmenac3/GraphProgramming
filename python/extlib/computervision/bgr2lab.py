import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("BGR to Lab", "extlib.computervision.bgr2lab",
                                   "",
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Convert BGR image to Lab image.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        return {"result": img}
