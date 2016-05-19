import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Bounding Boxes", "computervision.boundingbox",
                                   {},
                                   {"cnts": "Contours"},
                                   {"result": "Boxes"},
                                   "Calc bounding boxes for contour.", verbose)
        self.args = args

    def tick(self, value):

        result = []
        cnts = value["cnts"]
        for cnt in cnts:
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            result.append(box)

        return {"result": result}
