import cv2
import numpy as np

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Color Quantization", "extlib.computervision.colorquantization",
                                   {"k": 4},
                                   {"img": "Image"},
                                   {"img": "Image"},
                                   "Reduce the number of colors", verbose)
        self.args = args

    def tick(self, value):
        img = value["img"]
        Z = img.reshape((-1,3))

        # convert to np.float32
        Z = np.float32(Z)
        
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = self.args["k"]
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        img = res.reshape((img.shape))
        
        return {"img": img}
