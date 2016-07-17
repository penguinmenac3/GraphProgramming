try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("If", "stdlib.structures.if", "",
                                   {"condition":"Boolean", "val":"Object"},
                                   {"true": "Object", "false":"Object"},
                                   "If condition pass to true otherwise to false.", verbose)

    def tick(self, value):
        if value["condition"]:
            return {"true": value["val"], "false": None}
        else:
            return {"true": None, "false": value["val"]}
