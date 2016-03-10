try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Equal", "boolean.equal", 5,
                                   {"1": "Boolean", "2": "Boolean", "3": "Boolean", "4": "Boolean", "5": "Boolean"},
                                   {"result": "Boolean"}, "Checks if the first arg inputs are equal.", verbose)
        self.args = args

    def tick(self, value):
        result = True
        for i in range(self.args - 1):
            result = result and value[str(i+1)] == value[str(i + 2)]
        return {"result": result}
