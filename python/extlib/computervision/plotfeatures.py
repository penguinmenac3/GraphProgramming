import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Plot features", "computervision.plotfeatures",
                                   "",
                                   {"img": "Image", "features": "Array"},
                                   {"img": "Image"},
                                   "Plot features into an image.", verbose)

    def tick(self, value):
        img = value["img"].copy()
        kp = value["features"]
        if len(kp) > 0:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img=cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return {"img": img}
