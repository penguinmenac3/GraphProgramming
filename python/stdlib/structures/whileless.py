try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("While less", "stdlib.structures.whileless", "",
                                   {"initial":"Number", "val":"Number"},
                                   {"loop": "Number", "leave":"Number"},
                                   "Loop while initial is less than val.", verbose)

    def tick(self, value):
        if value["initial"] < value["val"]:
            return {"loop": value["initial"], "leave": None}
        else:
            return {"loop": None, "leave": value["initial"]}
