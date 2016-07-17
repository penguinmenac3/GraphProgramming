try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Arg const", "stdlib.boolean.argconst", "arg", {},
                                   {"result": "Boolean"}, "Get input from arguments.", verbose, True, False)
        self.args = args

    def tick(self, value):
        global registry
        return {"result": registry[self.args]}
