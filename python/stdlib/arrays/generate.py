try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import time


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Array Generator", "stdlib.arrays.generate",
                                   {"code": 'y = x', "range": 100, "repeating": False, "time": 1},
                                   {},
                                   {"result": "Array"},
                                   "Executes the argument function as python code.", verbose, True, False)
        self.args = args

    def isRepeating(self):
        return self.args["repeating"]

    def tick(self, value):
        if self.args["repeating"]:
            time.sleep(self.args["time"])

        result = []
        max_x = self.args["range"]

        for x in range(max_x):
            y = 0
            exec(self.args["code"])
            result.append(y)

        return {"result": result}
