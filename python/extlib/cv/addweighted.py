import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.left = args["left"]
		self.right = args["right"]

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		img = value["left"]
		img2 = value["right"]
		img = cv2.addWeighted(img, self.left, img2, self.right, 0)
		return {"result":img}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")