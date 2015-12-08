import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Trigger Number", "number.trigger", {"val":42, "time":1.0},
                                   {}, {"result": "Number"}, "Trigger value every time seconds.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        return {"result": self.args["val"]}
