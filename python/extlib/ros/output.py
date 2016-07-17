try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Publish", "extlib.ros.input", {"topic": "/image"},
                                   {"val": "Object"},
                                   {},
                                   "Publish on topic.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        val = value["val"]

        return {}
