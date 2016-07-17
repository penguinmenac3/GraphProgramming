import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Trigger string", "stdlib.string.trigger", {"val": "Hello World!", "time": 1.0},
                                   {},
                                   {"result": "String"},
                                   "Trigger string.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        return {"result": self.args["val"]}
