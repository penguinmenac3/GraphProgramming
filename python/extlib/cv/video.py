import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created input node.")
		self.args = args
		self.cap = cv2.VideoCapture(args["resource"])
		if not self.cap.isOpened():
			raise Exception("Cannot open the given resource: ", args["resource"])

	def isInput(self):
		return True

	def isRepeating(self):
		return True

	def tick(self, value):
		time.sleep(1/self.args["fps"])
		success = False
		success, img = self.cap.read()
		if not success:
			return {"result":None}
		return {"result":img}


def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")