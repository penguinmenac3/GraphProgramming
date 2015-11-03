import json
from subprocess import check_output as qx

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("A node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		return {"result":json.loads(value["val"])}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")