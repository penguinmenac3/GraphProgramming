import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Add Weighted", "computervision.addweighted",
                                   {"left": "Number", "right": "Number"},
                                   {"left": "Image", "right": "Image"},
                                   {"result": "Image"},
                                   "Add the two images weighted.", verbose)
        self.args = args

    def tick(self, value):
        left = self.args["left"]
        right = self.args["right"]
        img = value["left"]
        img2 = value["right"]
        img = cv2.addWeighted(img, left, img2, right, 0)
        return {"result": img}
