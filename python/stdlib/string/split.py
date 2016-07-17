try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Split", "stdlib.string.split", "", {"str":"String", "splitter":"String"},
                                   {"result": "Array"},
                                   "Split a string by a splitter.", verbose)

    def tick(self, value):
        return {"result": value["str"].split(value["splitter"])}
