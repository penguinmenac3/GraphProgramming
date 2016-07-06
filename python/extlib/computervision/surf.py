import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import sys
    
class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Surf", "computervision.surf",
                                   "",
                                   {"img": "Image"},
                                   {"img": "Image", "features":"Array", "descs":"Array"},
                                   "Detect surf features.", verbose)
        self.args = args
        self.surf = None

    def tick(self, value):
        if self.surf is None:
            #self.sift = cv2.xfeatures2d.SIFT_create()
            self.surf = cv2.xfeatures2d.SURF_create()
        img = value["img"]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        (kps, descs) = self.surf.detectAndCompute(gray, None)
        #img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return {"img": img, "features": kps, "descs": descs}
