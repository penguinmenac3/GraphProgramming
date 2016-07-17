try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Derive", "stdlib.arrays.derive", {"delta_index": 1},
                                   {"val": "Array"},
                                   {"result": "Array"},
                                   "Derive the array.", verbose, False, False)
        self.args = args

    def tick(self, value):
        val = value["val"]
        delta_index = self.args["delta_index"]
        if len(val) <= delta_index:
            return {"result": None}
        result = []
        for x in range(len(val) - delta_index):
            result.append(val[x+delta_index] - val[x])
        return {"result": result}
