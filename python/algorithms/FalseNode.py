class Node(object):
	def __init__(self, verbose):
		if verbose:
			print("Created input node.")

	def isInput(self):
		return True

	def tick(self, value):
		return {"result":False}


def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("returns")