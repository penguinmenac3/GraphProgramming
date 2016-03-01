import sys

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Print", "system.print",
                                   "",
                                   {"val": "String"},
                                   {},
                                   "Print input to console.", verbose)

    def tick(self, value):
        print(value["val"])
        sys.stdout.flush()
        return {}
