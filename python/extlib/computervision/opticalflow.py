try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import cv2
import numpy as np

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Optical Flow Farneback", "extlib.computervision.opticalflow", {},
                                   {"img": "Image"},
                                   {"img": "Image"},
                                   "Calculate the dense optical flow.", verbose)
        self.args = args
        self.prvs = None
        self.hsv = None

    def tick(self, value):
        result = None
        tag = None
        if "tags" in value and "img" in value["tags"]:
            tag = value["tags"]["img"]
        img = value["img"]

        if self.prvs is None:
            self.prvs = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            self.hsv = np.zeros_like(img)
            self.hsv[...,1] = 255
        else:
            cur = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(self.prvs,cur, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            self.hsv[...,0] = ang*180/np.pi/2
            self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            result = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)
            self.prvs = cur

        if tag:
            return {"img": result, "tags":{"img":tag}}
        else:
            return {"img": result}
