class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created sum Node.")

	def isInput(self):
		return False

	def isRepeating(self):
		return False

	def tick(self, value):
		if (value["initial"] < value["val"]):
			return {"loop":value["initial"], "leave":None}
		else:
			return {"loop":None, "leave":value["initial"]}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("Sums two inputs.")