import json
from subprocess import check_output as qx

class Node(object):
	def __init__(self, verbose, args):
		self.executablePath = args["executable"]
		self.escapeArgs = args["escapeArgs"]
		if verbose:
			print("A node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		arg = value["arg"]
		if self.escapeArgs:
			arg = value["arg"].replace("\\", "\\\\").replace("\"", "\\\"")

		cmd = self.executablePath + " " + arg
		output = qx(cmd, shell=True).decode("utf-8")
		return {"result":output}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")