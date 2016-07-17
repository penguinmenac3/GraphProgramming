from subprocess import check_output as qx

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Execute", "stdlib.system.executable",
                                   {"executable": "python graphex.py", "escapeArgs": False},
                                   {"arg": "String"},
                                   {"result": "String"},
                                   "Execute executable with given args.", verbose)
        self.args = args

    def tick(self, value):
        executablePath = self.args["executable"]
        escapeArgs = self.args["escapeArgs"]

        arg = value["arg"]
        if escapeArgs:
            arg = value["arg"].replace("\\", "\\\\").replace("\"", "\\\"")

        cmd = executablePath + " " + arg
        output = qx(cmd, shell=True).decode("utf-8")
        return {"result": output}
