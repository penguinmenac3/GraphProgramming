import json
from subprocess import check_output as qx

class Node(object):
	def __init__(self, verbose, args):
		self.executablePath = args
		if verbose:
			print("A node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		cmd = self.executablePath + " " + json.dumps(value).replace("\\", "\\\\").replace("\"", "\\\"")
		output = qx(cmd, shell=True).decode("utf-8")
		return json.loads(output)
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")