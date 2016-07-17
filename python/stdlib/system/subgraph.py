import json
from subprocess import check_output as qx

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Subgraph", "stdlib.system.subgraph",
                                   "DefaultGraph",
                                   {"arg": "Object"},
                                   {"result": "Object"},
                                   "Execute a subgraph.", verbose)
        self.args = args

    def tick(self, value):
        arg = json.dumps(value["arg"])

        cmd = "python ../python/graphex.py data/" + self.args + ".graph.json " + arg.replace("\\", "\\\\").replace("\"",
                                                                                                                   "\\\"")
        res = qx(cmd, shell=True).decode("utf-8")
        output = json.loads(res.strip())
        return {"result": output}
