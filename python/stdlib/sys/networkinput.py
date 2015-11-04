import json
import socket
import time

class Node(object):
	def __init__(self, verbose, args):
		self.host = args["host"]
		self.port = args["port"]
		if verbose:
			print("Created node.")

	def isInput(self):
		return True

	def isRepeating(self):
		return True
		
	def tick(self, value):
		line = None
		while line == None:
			try:
				self.socket = socket.socket()
				self.socket.connect((self.host, self.port))
				self.socketfile = self.socket.makefile()
				self.socket.send((json.dumps(value)+"\n").encode("utf-8"))
				line = self.socketfile.readline()
				self.socket.close()
			except (ConnectionRefusedError, ConnectionResetError):
				time.sleep(1)
				line = None
		return json.loads(line)
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")