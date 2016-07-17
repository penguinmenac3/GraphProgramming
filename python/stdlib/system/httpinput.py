try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

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

GET_REQUEST = None
POST_REQUEST = None

class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        path = self.path[1:] or "index.html"
        path = unquote(path)
        if path.startswith("/"):
            path = path[1:]
        GET = {}
        if path.contains("?"):
            args = path.split('?')[1].split('&')
            path = path.split('?')[0]

            for arg in args:
                t = arg.split('=')
                if len(t) > 1:
                    k, v = arg.split('=')
                    GET[k] = v

        #GET_REQUEST(self, path, GET)

    def do_POST(self):
        postvars = {}

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
            pass
        # print(postvars)
        for x in postvars:
            postvars[x] = postvars[x][0]
        #POST_REQUEST(self, path, postvars)

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("[WIP] HTTP Input", "stdlib.system.httpinput", {"port":80},
                                   {},
                                   {"get": "Object", "post": "Object", "put": "Object", "delete": "Object"},
                                   "Wait for http requests.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        getRes = None
        postRes = None
        putRes = None
        deleteRes = None
                
        if tag:
            return {"get": getRes, "post": postRes, "put": putRes, "delete": deleteRes, "tags":{"get": tag, "post": tag, "put": tag, "delete": tag}}
        else:
            return {"get": getRes, "post": postRes, "put": putRes, "delete": deleteRes}
