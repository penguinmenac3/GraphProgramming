import json
from subprocess import check_output as qx

class Node(object):
	def __init__(self, verbose):
		self.executablePath = "python ../python/external/executable.py"
		if verbose:
			print("Created test executable node.")

	def isInput(self):
		return False

	def tick(self, value):
		cmd = self.executablePath + " " + json.dumps(value).replace("\\", "\\\\").replace("\"", "\\\"")
		output = qx(cmd, shell=True).decode("utf-8")
		return json.loads(output)
		

def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("Calls another executable to process data.")