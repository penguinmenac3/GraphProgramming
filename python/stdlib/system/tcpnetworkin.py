import socket
import time
from threading import Thread
import select
import sys

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
        self.server = None
        self.sockets = []

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
            result["tags"] = {"result": {"sock":sock, "closeSock": self.close_sock}}
        else:
            sock.close()
        return result
                              
    def close_sock(self, sock):
        sock.close()
        self.sockets.remove(sock)

    def server_styled_pull(self, host, port, password):
        line = None
        if self.server is None:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind the socket to a public host, and a well-known port
            self.server.bind((host, port))
            # become a server socket
            self.server.listen(5)
            self.sockets.append(self.server)
        sock = None
        sf = None
        while sock is None:
            ready_to_read, ready_to_write, in_error = select.select(self.sockets, [], [], 1)
            if len(ready_to_read) > 0:
              sock = ready_to_read[0]
              if sock == self.server:
                sock, addr = self.server.accept() 
                if password is not None:
                  sf = sock.makefile()
                  if not sf.readline().rstrip('\n') == password:
                    sock.close()
                    sock = None
                    continue
                self.sockets.append(sock)
                sock = None
                continue
              try:
                sf = sock.makefile()
              except:
                self.close_sock(sock)
                sock = None
        line = sf.readline().rstrip('\n')
        return line, sock

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
                    line = sf.readline().rstrip('\n')
                else:
                    line = self.args["passDummy"]
                return line, s
            except (ConnectionRefusedError, ConnectionResetError):
                time.sleep(1)
                line = None
