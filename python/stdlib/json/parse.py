import json

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Parse Json", "stdlib.json.parse", "", {"val":"String"}, {"result": "Object"},
                                   "Parse a json string into an object.", verbose)

    def tick(self, value):
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
            return {"result": json.loads(value["val"]), "tags": {"result": tag}}
        return {"result": json.loads(value["val"])}
