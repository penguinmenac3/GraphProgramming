import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Leaky Integrator", "structures.leakyintegrator", {"time": 1.0, "decay": 1.0},
                                   {"val": "Number"},
                                   {"result": "Boolean"},
                                   "Leaky integrator.", verbose, True, True)
        self.args = args
        self.value = 0

    def isRepeating(self):
        return self.value > 0

    def tick(self, value):
        time.sleep(self.args["time"])
        self.value += value["val"]
        value["val"] = 0
        self.value -= self.args["decay"]
        return {"result": self.value > 0}
