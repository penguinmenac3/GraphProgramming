try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Splitflow", "default.splitflow5", "", {"val": "Object"},
                                   {"1": "Object", "2": "Object", "3": "Object", "4": "Object", "5": "Object"},
                                   "Splits the flow.", verbose)

    def tick(self, value):
        return {"1": value["val"], "2": value["val"], "3": value["val"], "4": value["val"], "5": value["val"]}
