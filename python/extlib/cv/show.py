import cv2
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.window_title = args["title"]
		self.img = None
		Thread(target=self.uithread).start()

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		self.img = value["img"]
		return {}

	def uithread(self):
		cv2.namedWindow(self.window_title)
		while True:
			if not self.img == None:
				cv2.imshow(self.window_title, self.img)
				if cv2.waitKey(2) == 27:
					global registry
					registry["kill"] = True
					break
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")