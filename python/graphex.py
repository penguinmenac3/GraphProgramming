import json

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
		if self.verbose:
			print(self.nodes)
			print(self.input_nodes)

		self.tryExecute(self.input_nodes.values())

	def tryExecute(self, nodes):
		for node in nodes:
			if self.checkIfCalculated(node.prevNodes):
				value = {}
				for key in node.inputs:
					resultNode = node.inputs[key]["node"]
					varname = node.inputs[key]["var"]
					value[key] = self.calculated[resultNode][varname]
				result = node.tick(value)
				self.calculated[node] = result
				self.tryExecute(node.nextNodes)

	def checkIfCalculated(self, nodes):
		for node in nodes:
			if node not in self.calculated:
				return False
		return True

if __name__ == "__main__":
	print("Not implemented yet.")