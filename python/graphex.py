import json

class GraphEx(object):
	def __init__(self, graph_path):
		data = open(graph_path, 'r').read()
		self.raw_graph = json.loads(data)
		self.findAndCreateNodes(self.raw_graph["nodes"])
		self.findAndCreateConnections(self.raw_graph["connections"])

	def findAndCreateNodes(self, nodelist):
		self.nodes = {}
		self.input_nodes = []
		for node in nodelist:
			try:
				print("Importing algorithms.%s" % node["code"])
				module = __import__("algorithms.%s" % node["code"], fromlist=["instance"])
			except ImportError:
				print("Cannot find implementation for node: " + node["code"])
			self.nodes[node["name"]] = module.instance()
			if self.nodes[node["name"]].isInput():
				self.input_nodes.append(self.nodes[node["name"]])

	def findAndCreateConnections(self, connectionlist):
		self.connections = {}
		for conn in connectionlist:
			inputNode = self.nodes[conn["input"]["node"]]
			outputNode = self.nodes[conn["output"]["node"]]
			mapping = {conn["input"]["output"]:conn["output"]["input"]}
			if inputNode not in self.connections:
				self.connections[inputNode] = []
			self.connections[inputNode].append({"output":outputNode,"mapping":mapping})

	def execute(self):
		print(self.nodes)
		print(self.input_nodes)
		print(self.connections)
		print("Not implemented yet.")

if __name__ == "__main__":
	GraphEx("../samples/Graph1.json").execute()
	GraphEx("../samples/Graph2.json").execute()