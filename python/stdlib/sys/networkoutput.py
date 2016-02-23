import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Network", "sys.networkoutput",
                                   {"host": "127.0.0.1", "port": 25555, "server": False, "password": None},
                                   {"msg": "String"},
                                   {"result": "String"},
                                   "Execute executable with given args.", verbose)
        self.args = args

    def tick(self, value):
        host = self.args["host"]
        port = self.args["port"]
        line = None
        while line is None:
            try:
                s = socket.socket()
                s.connect((host, port))
                s.send((value["msg"] + "\n").encode("utf-8"))
                s.close()
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
        return {}
