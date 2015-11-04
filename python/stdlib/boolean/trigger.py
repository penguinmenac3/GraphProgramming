import time

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created input node.")
		self.args = args

	def isInput(self):
		return True

	def isRepeating(self):
		return True

	def tick(self, value):
		time.sleep(self.args["time"])
		return {"result":self.args["val"]}


def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")