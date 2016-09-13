#!/usr/bin/python
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import parse_qs
    from urllib.request import unquote
except ImportError:
    # Python 2 legacy support
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from urlparse import parse_qs
    from urllib2 import unquote
from cgi import parse_header, parse_multipart
import os
import os.path
import signal
from threading import Thread
import subprocess
import sys
import socket
import time
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
import json
# or: from autobahn.asyncio.websocket import WebSocketServerProtocol

PORT_NUMBER = 8088
WS_PORT_NUMBER = 23352
HOST = "127.0.0.1"
execProcess = None
result = None
SERVER_URL = sys.argv[1] if len(sys.argv) == 2 else ""
DEBUG_WS = None
DEBUG_SOCK = None
DEBUG_KEY = "wasd" # TODO make generic uid
print("SERVER_URL: " + SERVER_URL)

def pollPipe():
    global execProcess
    global result
    while execProcess is not None:
        line = execProcess.stdout.readline().decode("utf-8")
        if line != '':
            #the real code does filtering here
            result = result + line.rstrip() + "\n"
        else:
            break
    execProcess = None


def pollErrPipe():
    global execProcess
    global result
    while execProcess is not None:
        line = execProcess.stderr.readline().decode("utf-8")
        if line != '':
            #the real code does filtering here
            result = result + line.rstrip() + "\n"
        else:
            break
    execProcess = None


def debugger():
    global DEBUG_WS
    global DEBUG_SOCK
    time.sleep(1)
    s = socket.socket()
    connected = False
    i = 0
    while not connected and i < 30:
        try:
            s.connect(("localhost", 25923))
            connected = True
        except:
            print("Connection refused")
            i += 1
            time.sleep(1)
    if i >= 30:
        print("Connection refused completely.")
        return
    DEBUG_SOCK = s
    print("Connected")
    sf = s.makefile()
    while True:
        try:
            line = sf.readline()
            if line == "":
                print("Connection closed")
                break
            if DEBUG_WS is not None:
                #print(line)
                DEBUG_WS.sendMessage(line, False)
        except:
            print("Closed with error.")
            break
    s.close()
    DEBUG_SOCK = None


class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        global DEBUG_WS
        global DEBUG_SOCK
        global DEBUG_KEY
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            if self is not DEBUG_WS:
                if payload == DEBUG_KEY:
                    DEBUG_WS = self
                else:
                    self.closedByMe()
            else:
                DEBUG_SOCK.send(payload)

    def onClose(self, wasClean, code, reason):
        global DEBUG_WS
        if DEBUG_WS is self:
            DEBUG_WS = None
        DEBUG_SOCK.close()
        print("WebSocket connection closed: {}".format(reason))


def debugWS():
    factory = WebSocketServerFactory(u"ws://"+HOST+":"+str(WS_PORT_NUMBER))
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(WS_PORT_NUMBER, factory)
    reactor.run()


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        path = self.path[1:] or "index.html"
        path = unquote(path)
        if path.startswith("/"):
            path = path[1:]
        if path.startswith("api"):
            GET = {}
            args = path.split('?')[1].split('&')

            for arg in args:
                t = arg.split('=')
                if len(t) > 1:
                    k, v = arg.split('=')
                    GET[k] = v
            self.handleAPI(GET)
            return

        path = "sites/" + path
        try:
            if path.endswith(".png"):
                f=open(path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            data = open(path, 'r').read()
            self.send_response(200)
            if (path.endswith(".css")):
                self.send_header('Content-type', 'text/css')
            elif (path.endswith(".js")):
                self.send_header('Content-type', 'text/js')
            else:
                self.send_header('Content-type', 'text/html')
            self.end_headers()
               # Send the html message
            data = data.replace("###REPLACE###", SERVER_URL)
            self.wfile.write(data.encode("utf-8"))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
               # Send the html message
            self.wfile.write("File not found!".encode("utf-8"))
        return

    def do_POST(self):
        path = self.path[1:] or "index.html"
        path = unquote(path)
        if path.startswith("/"):
            path = path[1:]
        if not path.startswith("api"):
            self.do_GET()
            return
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile.decode("utf-8"), pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length).decode("utf-8"),
                    keep_blank_values=1)
        else:
            postvars = {}
        #print(postvars)
        for x in postvars:
            postvars[x] = postvars[x][0]
        self.handleAPI(postvars)
        return

    def handleAPI(self, data):
        print(data)
        path = None
        global execProcess
        global result
        if "listGraphs" in data:
            graphs = []
            for root, dirs, files in os.walk(u'data'):
                for f in files:
                    if f.endswith('.graph.json'):
                        graphs.append(os.path.join(root, f))
            for root, dirs, files in os.walk(u'data/private'):
                for f in files:
                    if f.endswith('.graph.json'):
                        graphs.append(os.path.join(root, f))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write(json.dumps(graphs).encode("utf-8"))
            return
        if "startGraph" in data:
            #data["execGraph"] = re.sub(r'(\W|/)+', '', data["execGraph"])
            print(("Starting: " + data["startGraph"]))
            if execProcess is not None:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Canot start 2 processes.".encode("utf-8"))
                return
            cmd = "data/" + data["startGraph"] + ".graph.json"
            preex = None
            if "execEnv" in data and data["execEnv"] == "Lua":
                try:
                    preex = os.setsid
                except AttributeError:
                    print("Windows: Feature not availible.")
                cmd = ["../lua/graphex ../grapheditor/" + cmd + " debug"]
            else:
                try:
                    preex = os.setsid
                    cmd = ["python ../python/graphex.py " + cmd + " debug"]
                except AttributeError:
                    print("Windows: Feature not availible.")
                    cmd = ["python2", "../python/graphex.py ", cmd, "debug"]
            execProcess = subprocess.Popen(
                cmd,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                 shell=True, preexec_fn=preex)
            result = ""
            Thread(target=pollPipe).start()
            Thread(target=pollErrPipe).start()
            Thread(target=debugger).start()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
            return
        if "updateGraph" in data:
            if execProcess is None and result is None:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Process must be running".encode("utf-8"))
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
            if execProcess is None:
                result = None
            return
        if "killGraph" in data:
            if execProcess is None:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Process must be running".encode("utf-8"))
                return

            try:
                os.killpg(execProcess.pid, signal.SIGTERM)
            except AttributeError:
                print("Windows: Feature not availible.")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("".encode("utf-8"))
            return
        if "getnodes" in data:
            subprocess.call(["bash", "buildSpec", data["getnodes"]])
            path = "data/" + data["getnodes"] + ".nodes.json"
        if "getsrc" in data:
            node = data["getsrc"].decode("utf-8").replace(".", "/").replace("/lua", ".lua").replace("/py", ".py")
            path = "../" + node
            print(path)
        if "setsrc" in data:
            node = data["setsrc"].decode("utf-8").replace(".", "/").replace("/lua", ".lua").replace("/py", ".py")
            path = "../" + node
            print(os.path.dirname(path))
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            text_file = open(path, "w")
            text_file.write(data["value"])
            text_file.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("{'success':true}".encode("utf-8"))
            return
        if "getgraph" in data:
            path = "data/" + data["getgraph"] + ".graph.json"
        if path:
            try:
                data = open(path, 'r').read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                   # Send the html message
                self.wfile.write(data.encode("utf-8"))
                return
            except:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("File not found!".encode("utf-8"))
                return
        elif "setgraph" in data and "value" in data:
            text_file = open("data/" + data["setgraph"] + ".graph.json", "w")
            text_file.write(data["value"])
            text_file.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("{'success':true}".encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Invalid api operation.".encode("utf-8"))
        return


def webserver():
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print(('Started httpserver on port ' + str(PORT_NUMBER)))

        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
        running = False


def main():
    t = Thread(target=webserver)
    t.setDaemon(True)
    t.start()
    debugWS()

main()
