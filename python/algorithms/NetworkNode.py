import json
import socket

class Node(object):
	def __init__(self, verbose):
		self.host = "localhost"
		self.port = 25555
		self.socket = socket.socket()
		self.socket.connect((self.host, self.port))
		self.socketfile = self.socket.makefile()
		if verbose:
			print("Created test executable node.")

	def isInput(self):
		return False

	def tick(self, value):
		self.socket.send((json.dumps(value)+"\n").encode("utf-8"))
		line = self.socketfile.readline()
		return json.loads(line)
		

def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("Calls another executable to process data.")