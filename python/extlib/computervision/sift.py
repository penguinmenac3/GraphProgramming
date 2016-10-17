import sys
import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Sift", "extlib.computervision.sift",
                                   "",
                                   {"img": "Image"},
                                   {"img": "Image", "features":"Array", "descs":"Array"},
                                   "Detect sift features.", verbose)
        self.args = args
        self.sift = None

    def tick(self, value):
        if self.sift is None:
        	if cv2.__version__.startswith("2.4"):
        		print("Using fallback ORB instead of SIFT")
        		sys.stdout.flush()
        		self.sift = cv2.ORB()
        	else:
        		self.sift = cv2.xfeatures2d.SIFT_create()
        	#self.sift = cv2.xfeatures2d.SURF_create()
        img = value["img"]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (kps, descs) = self.sift.detectAndCompute(gray, None)

        return {"img": img, "features": kps, "descs": descs}
