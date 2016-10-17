import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import sys
    
class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Bounding Boxes", "extlib.computervision.boundingbox",
                                   {},
                                   {"cnts": "PolygonArray"},
                                   {"result": "PolygonArray"},
                                   "Calc bounding boxes for contour.", verbose)
        self.args = args

    def tick(self, value):

        result = []
        cnts = value["cnts"]
        for cnt in cnts:
            #print(cnt)
            #sys.stdout.flush()
            rect = cv2.minAreaRect(cnt)
            box = None
            if cv2.__version__.startswith("2.4"):
            	box = cv2.cv.BoxPoints(rect)
            else:
            	box = cv2.boxPoints(rect)
            box = np.int0(box)
            result.append(box)

        return {"result": result}
