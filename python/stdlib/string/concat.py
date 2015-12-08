try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("String Concat", "string.concat", "", {"left": "String", "right": "String"},
                                   {"result": "String"},
                                   "Concat the two strings.", verbose)

    def tick(self, value):
        return {"result": value["left"] + value["right"]}
