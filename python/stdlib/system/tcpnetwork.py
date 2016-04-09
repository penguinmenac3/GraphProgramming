import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("TCP Network", "system.tcpnetwork",
                                   {"host": "127.0.0.1", "port": 25555, "password": None},
                                   {"msg": "String"},
                                   {"result": "String"},
                                   "Send input over network and wait for result.", verbose)
        self.args = args

    def tick(self, value):
        host = self.args["host"]
        port = self.args["port"]
        password = self.args["password"]
        line = None
        while line is None:
            try:
                s = socket.socket()
                s.connect((host, port))
                sf = s.makefile()
                if password is not None:
                    s.send((password + "\n").encode("utf-8"))
                s.send((value["msg"] + "\n").encode("utf-8"))
                line = sf.readline()
                s.close()
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
        return {"result": line}
