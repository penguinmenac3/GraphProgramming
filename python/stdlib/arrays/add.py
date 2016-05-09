try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Add", "arrays.add", {},
                                   {"left": "Array", "right": "Array"},
                                   {"result": "Array"},
                                   "A constant input array.", verbose, False, False)
        self.args = args

    def tick(self, value):
        l = value["left"]
        r = value["right"]
        if len(l) != len(r):
            return {"result": None}
        result = []
        for x in range(len(l)):
            result.append(l[x] + r[x])
        return {"result": result}
