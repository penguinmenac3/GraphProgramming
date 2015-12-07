import json

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Parse Json", "json.parse", "", {"val":"String"}, {"result": "Object"},
                                   "Parse a json string into an object.", verbose)

    def tick(self, value):
        return {"result": json.loads(value["val"])}
