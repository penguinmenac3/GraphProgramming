import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("TCP Network", "system.tcpnetworkin",
                                   {"host": "127.0.0.1", "port": 25555, "server": True, "password": None, "passSocketAsTag": True, "passDummy": None},
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
        sock = None
        if not isServer:
            line, sock = self.client_styled_pull(host, port, password)
        else:
            line, sock = self.server_styled_pull(host, port, password)
        result = {"result": line}
        if self.args["passSocketAsTag"]:
            result["tags"] = {"result": sock}
        else:
            sock.close()
        return result

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
                if self.args["passDummy"] is None:
                    line = sf.readline()
                else:
                    line = self.args["passDummy"]
                return line, s
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
