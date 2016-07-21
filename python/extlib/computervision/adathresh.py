import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Adaptive Thresh", "extlib.computervision.adathresh",
                                   {"gaussian": False, "blockSize": 11, "C": 2, "inverted": False},
                                   {"img": "Image"},
                                   {"result": "Image"},
                                   "Adaptive threshold.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        tresh = cv2.THRESH_BINARY
        if self.args["inverted"]:
          tresh = cv2.THRESH_BINARY_INV
        if not self.args["gaussian"]:
            img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, tresh,self.args["blockSize"],self.args["C"])
        else:
            img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, tresh,self.args["blockSize"],self.args["C"])
        return {"result": img}
