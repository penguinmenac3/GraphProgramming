import json
import sys
import time
from threading import Thread
from collections import deque

class GraphEx(object):
	def __init__(self, graph_path, verbose = False):
		data = open(graph_path, 'r').read()
		self.verbose = verbose
		self.raw_graph = json.loads(data)
		self.findAndCreateNodes(self.raw_graph["nodes"])
		self.findAndCreateConnections(self.raw_graph["connections"])

	def findAndCreateNodes(self, nodelist):
		self.nodes = {}
		self.input_nodes = {}

		# Load all nodes.
		for node in nodelist:
			if node["name"] in self.nodes:
				raise Exception("Invalid Graph: Duplicate node name. All node names must be unique!")

			# Try to import the code required for a node.
			try:
				if self.verbose:
					print("Importing algorithms.%s" % node["code"])
				module = __import__("algorithms.%s" % node["code"], fromlist=["instance"])
			except ImportError:
				raise ImportError("Cannot find implementation for node: " + node["code"])

			# Create node and add lists for connecting them.
			currentNode = module.instance(self.verbose)
			currentNode.nextNodes = []
			currentNode.prevNodes = []
			currentNode.inputs = {}

			# Add the node to the internal lists for inputs and all nodes.
			self.nodes[node["name"]] = currentNode
			if self.nodes[node["name"]].isInput():
				self.input_nodes[node["name"]] = self.nodes[node["name"]]

	def findAndCreateConnections(self, connectionlist):
		self.connections = {}
		for conn in connectionlist:
			inputNode = self.nodes[conn["input"]["node"]]
			outputNode = self.nodes[conn["output"]["node"]]
			outputQualifier = conn["input"]["output"]
			inputQualifier = conn["output"]["input"]

			inputNode.nextNodes.append(outputNode)
			outputNode.prevNodes.append(inputNode)
			outputNode.inputs[inputQualifier] = {"node":inputNode,"var":outputQualifier}

	def execute(self):
		self.calculated = {}
		self.toCalculate = deque()
		self.activeCalculations = []
		if self.verbose:
			print(self.nodes)
			print(self.input_nodes)

		self.toCalculate.extend(self.input_nodes.values())
		self.tryExecute()

	def tryExecute(self):
		while self.toCalculate or self.activeCalculations:
			if not self.toCalculate:
				time.sleep(0.01)
				continue
			node = self.toCalculate.popleft()
			if self.checkIfCalculated(node.prevNodes) and node not in self.calculated and node not in self.activeCalculations:
				value = {}
				for key in node.inputs:
					resultNode = node.inputs[key]["node"]
					varname = node.inputs[key]["var"]
					value[key] = self.calculated[resultNode][varname]
				self.activeCalculations.append(node)
				Thread(target=self.executeNode, args=(node, value)).start()

	def executeNode(self, node, value):
		result = node.tick(value)
		self.calculated[node] = result
		self.toCalculate.extend(node.nextNodes)
		self.activeCalculations.remove(node)

	def checkIfCalculated(self, nodes):
		for node in nodes:
			if node not in self.calculated:
				return False
		return True

if __name__ == "__main__":
	for arg in sys.argv[1:]:
		GraphEx(arg).execute()
	if len(sys.argv) < 2:
		print("Usage: Pass graph json files to execute as parameters.")