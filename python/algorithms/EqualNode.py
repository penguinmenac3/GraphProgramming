class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.args = args

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		result = True
		for (i in range(args-1)):
			result = result && value[i] == value[i+1]
		return {"result":result}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")