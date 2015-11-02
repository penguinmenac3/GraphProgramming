class Node(object):
	def __init__(self, verbose):
		if verbose:
			print("Created sum Node.")

	def isInput(self):
		return False

	def tick(self, value):
		if (value["condition"]):
			return {"true":value["val"], "false":None}
		else:
			return {"true":None, "false":value["val"]}
		

def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("Sums two inputs.")