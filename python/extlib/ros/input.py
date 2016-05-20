try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Listen", "ros.input", {"topic": "/lidar_front"},
                                   {},
                                   {"result": "Object"},
                                   "Listen on topic.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        result = []

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
