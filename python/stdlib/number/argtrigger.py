import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Number Argument Trigger", "stdlib.number.argtrigger", {"val": "arg", "time": 1.0}, {},
                                   {"result": "Number"},
                                   "Pass the argument of the program.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        global registry
        return {"result": registry[self.args["val"]]}
