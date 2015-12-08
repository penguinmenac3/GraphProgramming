import time
import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Video", "cv.video",
                                   {"resource": 0, "fps": 30},
                                   {},
                                   {"result": "Image"},
                                   "Capture video.", verbose, True, True)
        self.args = args
        self.cap = None

    def tick(self, value):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.args["resource"])
            if not self.cap.isOpened():
                raise Exception("Cannot open the given resource: ", self.args["resource"])
        time.sleep(1/self.args["fps"])
        success = False
        success, img = self.cap.read()
        if not success:
            return {"result":None}
        return {"result":img}
