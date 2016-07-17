try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import time
import sys

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Image to distribution", "extlib.computervision.img2distribution",
                                   "",
                                   {"img": "Image"},
                                   {"result": "Array"},
                                   "Convert an image to a distribution.", verbose)

    def tick(self, value):
        #t = time.time()
        img = value["img"]
        width = 0
        height = 0
        try:
            height, width, shape = img.shape
        except:
            height, width = img.shape
        distribution = list(range(width))
        
        for x in range(width):
            p = 0.0
            for y in range(height):
                p += img[y, x] / 256.0
            distribution[x] = p / height

        #elapsed = time.time() - t
        #print(elapsed)
        #sys.stdout.flush()
        return {"result":distribution}
