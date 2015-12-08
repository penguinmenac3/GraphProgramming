try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Ends with", "string.endswith", "", {"str":"String", "ref":"String"},
                                   {"result": "Boolean"},
                                   "Check if a string ends with the reference.", verbose)

    def tick(self, value):
        return {"result": value["str"].endswith(value["ref"])}
