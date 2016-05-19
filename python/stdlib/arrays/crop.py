try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Crop Values", "arrays.crop", {"map_to_zero": 0, "map_to_max": 1},
                                   {"val": "Array"},
                                   {"result": "Array"},
                                   "Crop the array by value.", verbose, False, False)
        self.args = args

    def tick(self, value):
        val = value["val"]
        map_to_zero = self.args["map_to_zero"]
        map_to_max = self.args["map_to_max"]

        result = []
        for x in range(len(val)):
            tmp = val[x]
            if abs(tmp) < map_to_zero:
                tmp = 0
            if tmp > map_to_max:
                tmp = map_to_max
            if tmp < -map_to_max:
                tmp = -map_to_max
            result.append(tmp)
        return {"result": result}
