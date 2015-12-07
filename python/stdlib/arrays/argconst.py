try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Arg const", "arrays.argconst", "arg", {}, {"result":"String"}, "Get triggers from commandline.", verbose)
        self.args = args

    def tick(self, value):
        global registry
        return {"result":registry[self.args]}

if __name__ == "__main__":
    print(Node(False, []).toString())