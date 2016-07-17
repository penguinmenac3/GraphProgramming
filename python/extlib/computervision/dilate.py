import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Dilate", "extlib.computervision.dilate",
                                   {"size":5, "iterations": 1},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Dilate an image.", verbose)
        self.args = args

    def tick(self, value):
        size = self.args["size"]

        img = value["img"]
        kernel = np.ones((size, size),np.uint8)
        img = cv2.dilate(img, kernel, iterations = self.args["iterations"])
        return {"result": img}
