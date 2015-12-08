try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Greater than", "number.greater", "",
                                   {"left": "Number", "right": "Number"},
                                   {"result": "Number"},
                                   "Check if left > right.", verbose)

    def tick(self, value):
        return {"result": value["left"] > value["right"]}
