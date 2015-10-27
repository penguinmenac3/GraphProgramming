class Node(object):
	def __init__(self, verbose):
		if verbose:
			print("Created test input node.")

	def isInput(self):
		return True

	def tick(self, value):
		return {"test":3.14}


def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("returns 3.14")