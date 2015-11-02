class Node(object):
	def __init__(self, verbose):
		if verbose:
			print("Created sum Node.")

	def isInput(self):
		return False

	def tick(self, value):
		return {"1":value["val"], "2":value["val"], "3":value["val"], "4":value["val"], "5":value["val"]}
		

def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("Sums two inputs.")