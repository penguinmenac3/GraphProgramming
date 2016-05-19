import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Render Boxes", "computervision.renderboxes",
                                   {"r":255, "g":0, "b":0},
                                   {"img": "Image", "boxes": "Boxes"},
                                   {"result": "Image"},
                                   "Render boxes in image.", verbose)
        self.args = args

    def tick(self, value):
        boxes = value["boxes"]
        frame = value["img"].copy()

        for box in boxes:
            cv2.drawContours(frame, [box], 0, (self.args["b"], self.args["g"], self.args["r"]), 2)

        return {"result": frame}
