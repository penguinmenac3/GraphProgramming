import cv2

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Record", "cv.record",
                                   {"resource":"test.mp4"},
                                   {"img", "Image"},
                                   {},
                                   "Apply gaussian blur on image.", verbose)
        self.args = args
        self.writer = None

    def tick(self, value):
        img = value["img"]
        width = 0
        height = 0
        try:
            height, width, shape = img.shape
        except:
            height, width = img.shape
        if self.writer is None:
            self.writer = cv2.VideoWriter(self.args["resource"], -1, 20, (width, height))
            print("Recording: " + self.args["resource"] + " " + str(width) + "x" + str(height))
        # if not self.writer.isOpened():
        #	raise Exception("Cannot open the given resource: ", self.args["resource"])
        # frame = cv2.flip(img,0)
        frame = img
        self.writer.write(frame)
        return {}
