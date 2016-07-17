import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("In Range", "extlib.computervision.inrange",
                                   {"lower-hue": 0, "lower-saturisation": 0, "lower-value": 0, "upper-hue": 255, "upper-saturisation": 255, "upper-value": 255},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Apply an inRange operation on the image.", verbose)
        self.args = args

    def tick(self, value):
        lh = self.args["lower-hue"]
        ls = self.args["lower-saturisation"]
        lv = self.args["lower-value"]
        uh = self.args["upper-hue"]
        us = self.args["upper-saturisation"]
        uv = self.args["upper-value"]

        img = value["img"]
        lower = np.array((lh, ls, lv), dtype=np.uint8, ndmin=1)
        upper = np.array((uh, us, uv), dtype=np.uint8, ndmin=1)
        img = cv2.inRange(img, lower, upper)
        return {"result": img}
