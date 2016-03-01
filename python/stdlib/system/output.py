try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Output", "system.output",
                                   "arg",
                                   {"arg": "String"},
                                   {},
                                   "Set an output arg.", verbose)
        self.args = args

    def tick(self, value):
        global registry_output
        registry_output[self.args] = value["arg"]
        return {}
