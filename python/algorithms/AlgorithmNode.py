class Node(object):

	def __init__(self):
		print("Created test algorithm node.")

	def isInput(self):
		return False

	def tick(self, value):
		#print("Input: " + value)
		return {"testout":value["testin"] / 2}
		

def instance():
	return Node()

if __name__ == "__main__":
	print("Divides input by 2.")