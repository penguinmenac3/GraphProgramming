import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Find Contours", "extlib.computervision.findcontours",
                                   {},
                                   {"img": "Image"},
                                   {"result": "PolygonArray"},
                                   "Contours in an image.", verbose)
        self.args = args

    def tick(self, value):

        img = value["img"]
        #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #(cnts, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        im2, cnts, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        return {"result": cnts}
