try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("String Constant", "string.const", "Hello World!", {},
                                   {"result": "String"},
                                   "Pass the string arg as output.", verbose, True, False)
        self.args = args

    def tick(self, value):
        return {"result": self.args}
