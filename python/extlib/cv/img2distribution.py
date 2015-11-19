import cv2
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, verbose, args):
		if verbose:
			print("Created node.")
		self.blur_size = args

	def isInput(self):
		return False
		
	def isRepeating(self):
		return False

	def tick(self, value):
		img = value["img"]
		width = 0
		height = 0
		try:
			height, width, shape = img.shape
		except:
			height, width = img.shape
        distribution = list(range(width))
        
        for x in range(width):
            p = 0.0
            for y in range(height):
                p += img[y, x] / 256.0
            distribution[x] = p / height

		return {"result":distribution}
		

def instance(verbose, args):
	return Node(verbose, args)

if __name__ == "__main__":
	print("A node.")