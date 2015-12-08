try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Equal", "string.equal", 5,
                                   {"1": "String", "2": "String", "3": "String", "4": "String", "5": "String"},
                                   {"result": "Boolean"},
                                   "Check if values are equal.", verbose)
        self.args = args

    def tick(self, value):
        result = True
        for i in range(self.args - 1):
            result = result and value[i] == value[i + 1]
        return {"result": result}
