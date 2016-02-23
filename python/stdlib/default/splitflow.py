try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Splitflow", "default.splitflow", "", {"val": "Object"},
                                   {"left": "Object", "right": "Object"},
                                   "Splits the flow.", verbose)

    def tick(self, value):
        return {"left": value["val"], "right": value["val"]}
