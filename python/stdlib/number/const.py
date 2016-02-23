try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Number Constant", "number.const", 1.0, {},
                                   {"result": "Number"},
                                   "Pass the number arg as output.", verbose, True, False)
        self.args = args

    def tick(self, value):
        return {"result": self.args}
