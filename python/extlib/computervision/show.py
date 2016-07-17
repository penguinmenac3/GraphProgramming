import cv2
from threading import Thread

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Show", "extlib.computervision.show",
                                   {"title": "Debug View", "fullscreen": True},
                                   {"img": "Image"},
                                   {},
                                   "Show an image.", verbose, False, False, True)
        self.args = args
        self.started = False
        self.img = None

    def tick(self, value):
        window_title = self.args["title"]
        if not self.started:
            if not self.args["fullscreen"]:
            	cv2.namedWindow(window_title)
            else:
            	cv2.namedWindow(window_title, cv2.WND_PROP_FULLSCREEN)          
            	cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
            self.started = True
        self.img = value["img"]
        cv2.imshow(window_title, self.img)
        if cv2.waitKey(2) == 27:
            global registry
            registry["kill"] = True
        return {}            
                
