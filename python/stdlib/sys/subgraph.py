import json
from subprocess import check_output as qx

class Node(object):
	def __init__(self, verbose, args):
		self.args = args
		if verbose:
			print("A node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		arg = json.dumps(value["arg"])

		cmd = "python ../python/graphex.py data/" + self.args + ".graph.json " + arg.replace("\\", "\\\\").replace("\"", "\\\"")
		res = qx(cmd, shell=True).decode("utf-8")
		output = json.loads(res.strip())
		return {"result":output}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")