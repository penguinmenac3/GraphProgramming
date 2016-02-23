import cv2
from threading import Thread

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Show", "cv.show",
                                   {"title": "Debug View"},
                                   {"img": "Image"},
                                   {},
                                   "Show an image.", verbose)
        self.args = args
        self.started = False
        self.img = None

    def tick(self, value):
        if not self.started:
            Thread(target=self.uithread).start()
            self.started = True
        self.img = value["img"]
        return {}

    def uithread(self):
        window_title = self.args["title"]
        cv2.namedWindow(window_title)
        while True:
            if not self.img is None:
                cv2.imshow(window_title, self.img)
                if cv2.waitKey(2) == 27:
                    global registry
                    registry["kill"] = True
                    break
