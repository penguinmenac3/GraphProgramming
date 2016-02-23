try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Subtract", "number.subtract", "",
                                   {"left": "Number", "right": "Number"},
                                   {"result": "Number"},
                                   "Subtract right from left.", verbose)

    def tick(self, value):
        return {"result": value["left"] - value["right"]}
