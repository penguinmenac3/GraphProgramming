class Node(object):
	
	def __init__(self):
		print("Created test output node.")

	def isInput(self):
		return False

	def tick(self, value):
		print(value["testres"])
		return {}

		
def instance():
	return Node()

if __name__ == "__main__":
	print("Prints whatever is passed.")