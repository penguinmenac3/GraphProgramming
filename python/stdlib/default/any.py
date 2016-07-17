try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Accept any input", "stdlib.default.any", "", {"val":"Object"}, {"result": "Object"},
                                   "If any input is present pass it.", verbose, loopback="val")

    def tick(self, value):
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
            return {"result": value["val"], "tags": {"result": tag}}
        return {"result": value["val"]}
