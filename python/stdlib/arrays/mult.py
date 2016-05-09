try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Multiply", "arrays.mult", {},
                                   {"left": "Array", "right": "Array"},
                                   {"result": "Double"},
                                   "Multiply two values as scalar product.", verbose, False, False)
        self.args = args

    def tick(self, value):
        l = value["left"]
        r = value["right"]
        if len(l) != len(r):
            return {"result": None}
        result = 0
        for x in range(len(l)):
            result += l[x] * r[x]
        return {"result": result}
