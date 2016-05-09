try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Multiply (:Matrix)", "arrays.multInflate", {},
                                   {"left": "Array", "right": "Array"},
                                   {"result": "Matrix"},
                                   "Multiply two values as product resulting in a matrix.", verbose, False, False)
        self.args = args

    def tick(self, value):
        l = value["left"]
        r = value["right"]
        result = []
        for x in range(len(l)):
            result.append([])
            for y in range(len(r)):
                result[x].append(l[x] * r[y])
        return {"result": result}
