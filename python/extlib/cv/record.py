import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created input node.")
		self.args = args
		self.writer = None

	def isInput(self):
		return True

	def isRepeating(self):
		return True

	def tick(self, value):
		img = value["img"]
		width = 0
		height = 0
		try:
			height, width, shape = img.shape
		except:
			height, width = img.shape
		if self.writer == None:
			self.writer = cv2.VideoWriter(self.args["resource"], -1, 20, (width,height))
			print("Recording: " + self.args["resource"] + " "  + str(width) + "x" + str(height))
		#if not self.writer.isOpened():
		#	raise Exception("Cannot open the given resource: ", self.args["resource"])
		#frame = cv2.flip(img,0)
		frame = img
		self.writer.write(frame)
		return {}


def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node")