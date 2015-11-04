import time

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.args = args
		self.value = 0

	def isInput(self):
		return False

	def isRepeating(self):
		return self.value > 0

	def tick(self, value):
		time.sleep(self.args["time"])
		self.value += value["val"]
		value["val"] = 0;
		self.value -= self.args["decay"]
		return {"result":self.value > 0}


def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")