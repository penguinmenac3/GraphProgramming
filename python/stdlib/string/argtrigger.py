import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("String Argument Trigger", "stdlib.string.argtrigger", {"val": "arg", "time": 1.0}, {},
                                   {"result": "String"},
                                   "Pass the argument of the program.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        global registry
        return {"result": registry[self.args["val"]]}
