try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Or", "stdlib.boolean.or", "", {"left": "Boolean", "right": "Boolean"},
                                   {"result": "Boolean"}, "Output the or of the inputs.", verbose)

    def tick(self, value):
        return {"result": value["left"] or value["right"]}
