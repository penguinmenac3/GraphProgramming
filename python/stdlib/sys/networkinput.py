import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Network Input", "sys.networkinput",
                                   {"host": "127.0.0.1", "port": 25555, "server": False, "password": None},
                                   {},
                                   {"result": "String"},
                                   "Wait for input over network.", verbose, True, True)
        self.args = args

    def tick(self, value):
        host = self.args["host"]
        port = self.args["port"]
        password = None
        isServer = self.args["server"]
        if "password" in self.args and self.args["password"] is not None:
            password = self.args["password"]
        line = None
        if not isServer:
            line = self.client_styled_pull(host, port, password)
        else:
            line = self.server_styled_pull(host, port, password)
        return line

    def server_styled_pull(self, host, port, password):
        line = None
        return line

    def client_styled_pull(self, host, port, password):
        line = None
        while line is None:
            try:
                s = socket.socket()
                s.connect((host, port))
                sf = s.makefile()
                if password is not None:
                    s.send((password + "\n").encode("utf-8"))
                line = sf.readline()
                s.close()
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
        return line
