import time
try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Trigger", "boolean.trigger", {"val":True, "time":1.0}, {},
                                   {"result": "Boolean"}, "Trigger arg.val every arg.time s.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        return {"result":self.args["val"]}
