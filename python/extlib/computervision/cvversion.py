import cv2

try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("CV Version", "extlib.computervision.cvversion", {},
                                   {},
                                   {"result": "String"},
                                   "Outputs the cv version.", verbose)
        self.args = args

    def tick(self, value):
        return {"result": cv2.__version__}
