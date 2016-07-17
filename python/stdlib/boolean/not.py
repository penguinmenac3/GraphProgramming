try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Not", "stdlib.boolean.not", "", {"val": "Boolean"},
                                   {"result": "Boolean"}, "Output the inverted input.", verbose)

    def tick(self, value):
        return {"result": not value["val"]}
