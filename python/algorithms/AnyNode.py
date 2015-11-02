class Node(object):
	def __init__(self, verbose):
		if verbose:
			print("Created node.")

	def isInput(self):
		return False

	def tick(self, value):
		return {"result":value["val"]}
		

def instance(verbose):
	return Node(verbose)

if __name__ == "__main__":
	print("Divides input by 2.")