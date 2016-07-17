try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Index of", "stdlib.string.indexof", "",
                                   {"str": "String", "ref": "String", "offset": "Number"},
                                   {"result": "Number"},
                                   "Get the index of a ref in a string.", verbose)

    def tick(self, value):
        return {"result": value["str"].find(value["ref"], beg=value["offset"])}
