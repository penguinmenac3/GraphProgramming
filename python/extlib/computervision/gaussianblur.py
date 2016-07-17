import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Gaussian Blur", "extlib.computervision.gaussianblur",
                                   4,
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Apply gaussian blur on image.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.GaussianBlur(img, (0, 0), self.args * 2 + 1)
        return {"result": img}
