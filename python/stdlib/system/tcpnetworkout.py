import socket
import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("TCP Network", "system.tcpnetworkout",
                                   {"host": "127.0.0.1", "port": 25555, "server": False, "password": None, "closeAfterSend": True},
                                   {"msg": "String"},
                                   {},
                                   "Send message over tcp network.", verbose)
        self.args = args

    def tick(self, value):
        host = self.args["host"]
        port = self.args["port"]
        s = None
        if "tags" in value and "msg" in value["tags"]:
            s = value["tags"]["msg"]
            
        success = False
        while not success:
          try:
            if s is None:
            	s = socket.socket()
            	s.connect((host, port))
            s.send((value["msg"] + "\n").encode("utf-8"))
            if self.args["closeAfterSend"]:
            	s.close()
            success = True
          except (ConnectionRefusedError, ConnectionResetError):
            if "tags" in value and "msg" in value["tags"]:
                return {}
            time.sleep(1)
            s = None
        return {}
