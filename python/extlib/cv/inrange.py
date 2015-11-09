import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.lh = args["lh"]
		self.ls = args["ls"]
		self.lv = args["lv"]
		self.uh = args["uh"]
		self.us = args["us"]
		self.uv = args["uv"]

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		img = value["img"]
		lower = np.array((self.lh, self.ls, self.lv), dtype=np.uint8, ndmin=1)
		upper = np.array((self.uh, self.us, self.uv), dtype=np.uint8, ndmin=1)
		img = cv2.inRange(img, lower, upper)
		return {"result":img}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")