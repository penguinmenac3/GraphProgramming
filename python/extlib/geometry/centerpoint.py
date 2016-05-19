try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Centerpoint", "geometry.centerpoint", {},
                                   {"val": "Polygon"},
                                   {"result": "Point"},
                                   "Calculates average for polygon.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        arr = value["val"]
        x = 0
        y = 0
        for p in arr:
            x += p[0]
            y += p[1]
        x /= len(arr)
        y /= len(arr)
        result = [x, y]

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
