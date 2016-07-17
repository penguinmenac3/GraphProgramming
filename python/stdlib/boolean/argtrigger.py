import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Arg trigger", "stdlib.boolean.argconst", {"val":"arg", "time":1.0}, {},
                                   {"result": "Boolean"}, "Get input from arguments.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        global registry
        return {"result": registry[self.args["val"]]}
