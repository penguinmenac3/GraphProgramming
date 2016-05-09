try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Array const", "arrays.const", {"vals": [0, 1, 2, 3, 4, 5]},
                                   {},
                                   {"result": "Array"},
                                   "A constant input array.", verbose, True, False)
        self.args = args

    def tick(self, value):
        return {"result": self.args["vals"]}
