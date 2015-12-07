try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Const", "boolean.const", True, {},
                                   {"result": "Boolean"}, "Output the arg.", verbose, True, False)
        self.args = args

    def tick(self, value):
        return {"result": self.args}
