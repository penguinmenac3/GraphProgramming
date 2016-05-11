try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Splitflow 2", "default.splitflow", "", {"val": "Object"},
                                   {"left": "Object", "right": "Object"},
                                   "Splits the flow.", verbose)

    def tick(self, value):
        tags = {}
        if "tags" in value and "val" in value["tags"]:
            tags = {"left": value["tags"]["val"], "right": value["tags"]["val"]}
        return {"tags": tags, "left": value["val"], "right": value["val"]}
