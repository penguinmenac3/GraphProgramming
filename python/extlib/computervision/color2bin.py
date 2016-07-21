import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("2 Colors to Bin", "extlib.computervision.color2bin",
                                   {"imgSize": 80},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Adaptive threshold.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        
        lower = np.array((1, 1, 1), dtype=np.uint8, ndmin=1)
        upper = np.array((255, 255, 255), dtype=np.uint8, ndmin=1)
        mask = cv2.inRange(img, lower, upper)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[:, :, 0] = 127
        img[:, :, 2] = 127
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tresh = cv2.THRESH_BINARY_INV
        img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, tresh,self.args["imgSize"]-1, 0, mask=mask)
        
        #img = cv2.bitwise_and(img,img,mask = mask)
        return {"result": img}
