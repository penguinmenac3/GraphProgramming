try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("And", "boolean.and", "", {"left": "Boolean", "right": "Boolean"},
                                   {"result": "Boolean"}, "Combine inputs with and.", verbose)
        self.args = args

    def tick(self, value):
        return {"result": value["left"] and value["right"]}
