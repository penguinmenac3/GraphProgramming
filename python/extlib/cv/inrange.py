import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("In Range", "cv.inrange",
                                   {"lh": 0, "ls": 0, "lv": 0, "uh": 255, "us": 255, "uv": 255},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Apply an inRange operation on the image.", verbose)
        self.args = args

    def tick(self, value):
        lh = self.args["lh"]
        ls = self.args["ls"]
        lv = self.args["lv"]
        uh = self.args["uh"]
        us = self.args["us"]
        uv = self.args["uv"]

        img = value["img"]
        lower = np.array((lh, ls, lv), dtype=np.uint8, ndmin=1)
        upper = np.array((uh, us, uv), dtype=np.uint8, ndmin=1)
        img = cv2.inRange(img, lower, upper)
        return {"result": img}
