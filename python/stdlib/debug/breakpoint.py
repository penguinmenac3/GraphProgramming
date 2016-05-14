try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
try:
    import builtins
except ImportError:
    import __builtin__ as builtins


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Breakpoint", "debug.breakpoint", {},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Stops the execution until it's signaled to continue.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        if "debugger" in builtins.registry:
            builtins.registry["debugger"].wait_for("continue_"+self.node_uid)

        result = value["val"]

        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
