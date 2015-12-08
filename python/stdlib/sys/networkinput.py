import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Network Input", "sys.networkinput",
                                   {"host": "127.0.0.1", "port": 25555},
                                   {},
                                   {"result": "String"},
                                   "Wait for input over network.", verbose, True, True)
        self.args = args

    def tick(self, value):
        host = self.args["host"]
        port = self.args["port"]
        line = None
        while line is None:
            try:
                s = socket.socket()
                s.connect((host, port))
                sf = s.makefile()
                line = sf.readline()
                s.close()
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
        return line
