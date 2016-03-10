import time
import cv2
import cv2.cv as cv

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Video", "computervision.video",
                                   {"resource": 0, "fps": 30},
                                   {},
                                   {"result": "Image"},
                                   "Capture video.", verbose, True, True)
        self.args = args
        self.cap = None

    def set_res(self, x,y):
        self.cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
        self.cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
        return self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH), self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

    def tick(self, value):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.args["resource"])
            # self.set_res(1024.0, 768.0)
            self.set_res(1280,720)
            if not self.cap.isOpened():
                raise Exception("Cannot open the given resource: ", self.args["resource"])
        time.sleep(1/self.args["fps"])
        success = False
        success, img = self.cap.read()
        if not success:
            return {"result":None}
        return {"result":img}
