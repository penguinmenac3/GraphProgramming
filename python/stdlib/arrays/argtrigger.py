import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Arg trigger", "arrays.argtrigger", {"val": "arg", "time": 1.0}, {},
                                   {"result": "String"}, "Get triggers from commandline.", verbose, True, True)
        self.args = args

    def tick(self, value):
        time.sleep(self.args["time"])
        global registry
        return {"result": registry[self.args["val"]]}


if __name__ == "__main__":
    print(Node(False, []).toString())
