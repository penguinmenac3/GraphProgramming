class Node(object):
	def __init__(self):
		print("Created test input node.")

	def isInput(self):
		return True

	def tick(self):
		#print("Input: " + value)
		return {"test":3.14}


def instance():
	return Node()

if __name__ == "__main__":
	print("returns 3.14")