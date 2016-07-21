import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Invert Mask", "extlib.computervision.invertmask",
                                   {},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Invert the mask white and black.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        img = cv2.bitwise_not(img)
        return {"result": img}
