import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Sift", "computervision.sift",
                                   "",
                                   {"img": "Image"},
                                   {"img": "Image", "features":"Array"},
                                   "Detect sift features.", verbose)
        self.args = args
        self.sift = None

    def tick(self, value):
        if self.sift is None:
            self.sift = cv2.xfeatures2d.SIFT_create()
            #self.sift = cv2.SURF(400)
        img = value["img"]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kp = self.sift.detect(gray, None)

        return {"img": img, "features": kp}
