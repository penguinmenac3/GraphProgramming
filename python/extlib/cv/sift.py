import cv2
import numpy as np
from threading import Thread

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.sift = cv2.xfeatures2d.SIFT_create()
		#self.sift = cv2.SURF(400)

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		img = value["img"]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		kp = self.sift.detect(gray, None)

		return {"img":img, "features":kp}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")
