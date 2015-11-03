class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		return {"result":value["left"] - value["right"]}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")