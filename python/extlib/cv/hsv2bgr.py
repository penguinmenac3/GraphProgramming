import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		img = value["img"]
		img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
		return {"result":img}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")