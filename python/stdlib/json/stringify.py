import json

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Stringify Json", "json.stringify", "", {"val": "Object"}, {"result": "String"},
                                   "Makes a json string out of an object.", verbose)

    def tick(self, value):
        return {"result": json.dumps(value["val"])}
