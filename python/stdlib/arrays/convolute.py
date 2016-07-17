try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Convolute", "stdlib.arrays.convolute", {},
                                   {"data": "Array", "kernel": "Array"},
                                   {"result": "Array"},
                                   "Convolute two arrays.", verbose, False, False)
        self.args = args

    def tick(self, value):
        l = value["data"]
        r = value["kernel"]
        result = []
        rl = len(r)
        for x in range(len(l)):
            result.append(0)
            for y in range(len(r)):
                ind = x - rl/2 + y
                if 0 <= ind < len(l):
                    result[x] += l[ind] * r[y]

        return {"result": result}
