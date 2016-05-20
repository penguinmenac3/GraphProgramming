try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import math
import numpy as np


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Euler 2 Image", "geometry.plotpointarraycv", {"img_size":320, "view_size":10.0},
                                   {"val": "PointArray"},
                                   {"result": "Image"},
                                   "Plot to cv_image.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        val = value["val"]
        scale = self.args["img_size"] / self.args["view_size"]

        img = np.zeros((self.args["img_size"], self.args["img_size"], 3), np.uint8)

        for i in range(len(val)):
            x = val[i][0] * scale
            y = val[i][1] * scale
            ix = int(self.args["img_size"]/2 - x)
            iy = int(self.args["img_size"]/2 - y)
            if 0 <= ix < self.args["img_size"] and 0 <= iy < self.args["img_size"]:
                img[ix, iy] = (255, 255, 255)
                
        result = img

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
