try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Number Argument", "number.argconst", "arg", {}, {"result": "Number"},
                                   "Pass the argument of the program.", verbose, True, False)
        self.args = args

    def tick(self, value):
        global registry
        return {"result": registry[self.args]}
