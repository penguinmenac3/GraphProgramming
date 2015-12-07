import cv2
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

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
		kp = value["features"]
		if len(kp) > 0:
			gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			img = cv2.drawKeypoints(gray,kp) # whats wrong here?
		return {"img":img}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")
