try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Sum", "stdlib.number.sum", "",
                                   {"left": "Number", "right": "Number"},
                                   {"result": "Number"},
                                   "Sum left and right.", verbose)

    def tick(self, value):
        return {"result": value["left"] + value["right"]}
