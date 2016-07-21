import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Mask", "extlib.computervision.mask",
                                   "",
                                   {"img": "Image", "mask": "Image"},
                                   {"result": "Image"},
                                   "Apply a mask.", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        mask = value["mask"]
        img = cv2.bitwise_and(img,img,mask = mask)
        return {"result": img}
