try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Divide", "number.div", "", {"left":"Number", "right":"Number"},
                                   {"result": "Number"},
                                   "Divide left by right.", verbose)

    def tick(self, value):
        return {"result": value["left"] / value["right"]}
