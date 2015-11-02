#!/usr/bin/python
try:
    from http.server import BaseHTTPRequestHandler,HTTPServer
    from urllib.parse import parse_qs
    from urllib.request import unquote
except ImportError:
    # Python 2 legacy support
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
    from urlparse import parse_qs
    from urllib2 import unquote
from cgi import parse_header, parse_multipart
import socket
import sys
import os
from threading import Thread
import time
from subprocess import check_output as qx
import re

PORT_NUMBER = 8088

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        path = self.path[1:] or "index.html"
        path = unquote(path)
        if path.startswith("api"):
            GET={}
            args=path.split('?')[1].split('&')

            for arg in args: 
                t=arg.split('=')
                if len(t)>1: k,v=arg.split('='); GET[k]=v
            self.handleAPI(GET)
            return

        path = "sites/" + path
        try:
            data = open(path, 'r').read()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
               # Send the html message
            self.wfile.write(data.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
               # Send the html message
            self.wfile.write("File not found!".encode("utf-8"))
        return

    def do_POST(self):
        path = self.path[1:] or "index.html"
        path = unquote(path)
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
        if "execGraph" in data:
            data["execGraph"] = re.sub(r'\W+', '', data["execGraph"])
            print("Executing: " + data["execGraph"])
            cmd = "python ../python/graphex.py data/" + data["execGraph"] + ".graph.json"
            output = qx(cmd, shell=True).decode("utf-8")
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(output.encode("utf-8"))
            return
        if "getnodes" in data:
            path = "data/" + data["getnodes"] + ".nodes.json"
        if "getgraph" in data:
            path = "data/" + data["getgraph"] + ".graph.json"
        if path:
            try:
                data = open(path, 'r').read()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                   # Send the html message
                self.wfile.write(data.encode("utf-8"))
                return
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write("File not found!".encode("utf-8"))
                return
        elif "setgraph" in data and "value" in data:
            text_file = open("data/" + data["setgraph"] + ".graph.json", "w")
            text_file.write(data["value"])
            text_file.close()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("{'success':true}".encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("Invalid api operation.".encode("utf-8"))
        return

try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print('Started httpserver on port ' + str(PORT_NUMBER))

        #Wait forever for incoming htto requests
        server.serve_forever()

except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
        running = False
