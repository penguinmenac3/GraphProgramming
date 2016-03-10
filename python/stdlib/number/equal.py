try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Equal", "number.equal", 5,
                                   {"1": "Number", "2": "Number", "3": "Number", "4": "Number", "5": "Number"},
                                   {"result": "Boolean"},
                                   "Check if values are equal.", verbose)
        self.args = args

    def tick(self, value):
        result = True
        for i in range(self.args - 1):
            result = result and value[str(i+1)] == value[str(i + 2)]
        return {"result": result}
