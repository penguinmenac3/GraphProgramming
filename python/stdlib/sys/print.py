import sys

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		print(value["val"])
		sys.stdout.flush()
		return {}


def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")