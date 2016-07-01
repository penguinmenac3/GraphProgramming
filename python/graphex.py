import json
import sys
import time
from threading import Thread
from threading import Lock
import debugger
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from Queue import Queue

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

builtins.registry = {}
builtins.registry_output = {}
builtins.shutdown_hook = []

class GraphEx(object):
    def __init__(self, graph_path, verbose = False):
        self.nodes = {}
        self.input_nodes = {}
        self.lock = Lock()

        # Open the graph and parse it as json.
        data = open(graph_path, 'r').read()
        self.verbose = verbose
        self.raw_graph = json.loads(data)

        # Now build a graph that we can work with efficiently.
        self.findAndCreateNodes(self.raw_graph["nodes"])
        self.findAndCreateConnections(self.raw_graph["connections"])

    def findAndCreateNodes(self, nodelist):
        # Empty nodes and input nodes list.
        self.nodes = {}
        self.input_nodes = {}

        # Load all nodes.
        for node in nodelist:
            if node["name"] in self.nodes:
                raise Exception("Invalid Graph: Duplicate node name. All node names must be unique!")

            # Try to import the code required for a node.
            try:
                codeName = node["code"]
                if self.verbose:
                    print("Importing stdlib.%s" % codeName)
                module = __import__("stdlib.%s" % codeName, fromlist=["Node"])
            except ImportError:
                module = None
            # Try to import the code required for a node.
            if not module:
                try:
                    codeName = node["code"]
                    if self.verbose:
                        print("Importing extlib.%s" % codeName)
                    module = __import__("extlib.%s" % codeName, fromlist=["Node"])
                except ImportError:
                    module = None
            # Search in users private lib.
            if not module:
                try:
                    codeName = node["code"]
                    if self.verbose:
                        print("Importing privatelib.%s" % codeName)
                    module = __import__("privatelib.%s" % codeName, fromlist=["Node"])
                except ImportError:
                    raise ImportError("Cannot find implementation for node: " + node["code"])

            # Create node and add lists for connecting them.
            currentNode = module.Node(self.verbose, node["args"])
            currentNode.node_uid = node["name"]
            currentNode.nextNodes = []
            currentNode.prevNodes = []
            currentNode.ins = {}
            currentNode.outs = {}
            currentNode.inputBuffer = {"tags":{}}

            # Add the node to the internal lists for inputs and all nodes.
            self.nodes[node["name"]] = currentNode
            if self.nodes[node["name"]].isInput():
                self.input_nodes[node["name"]] = self.nodes[node["name"]]

    def findAndCreateConnections(self, connectionlist):
        self.connections = {}
        for conn in connectionlist:
            # Find all nodes and outputs as well as inputs.
            inputNode = self.nodes[conn["input"]["node"]]
            outputNode = self.nodes[conn["output"]["node"]]
            outputQualifier = conn["input"]["output"]
            inputQualifier = conn["output"]["input"]

            # Link the nodes together
            inputNode.nextNodes.append(outputNode)
            if outputQualifier not in inputNode.outs:
                inputNode.outs[outputQualifier] = []
            inputNode.outs[outputQualifier].append({"node":outputNode,"var":inputQualifier});
            outputNode.prevNodes.append(inputNode)
            outputNode.ins[inputQualifier] = {"var":outputQualifier}
    def prepareExecution(self):
        # Initialize all lists.
        self.toCalculate = []
        self.toCalculateMainThread = []
        self.activeCalculations = []
        self.ops = 0
        self.done_tasks = Queue()

        # add the input nodes to the nodes that should be calculated.
        self.toCalculate.extend(self.input_nodes.values())

    def executeThreaded(self):        
        t = Thread(target=self.execute)
        t.setDaemon(True)
        t.start()
        
        # Execute nodes until there is no more nodes to calculate and no nodes in calculation.
        while self.shouldStillRun():
            # When there are only active calculations and nothing new, wait.
            if not self.toCalculateMainThread:
                time.sleep(0.01)
                continue

            self.lock.acquire()
            # Select the node to execute and check if it can be executed.
            node = self.toCalculateMainThread[0]
            self.toCalculateMainThread = [value for value in self.toCalculateMainThread if value != node]
            if node in self.activeCalculations:
                self.toCalculateMainThread.append(node)
                self.lock.release()
                continue
            
            if self.checkIfReady(node):
                # Prepare the input value set for the node.
                abort = False
                for key in node.inputBuffer:
                    if node.inputBuffer[key] is None:
                        abort = True
                        break

                if not abort:
                    # Add the node to the active calculations list and start a calculation thread.
                    self.activeCalculations.append(node)
                    self.lock.release()
                    self.executeNode(node, node.inputBuffer)
            else:
                self.lock.release()
                    
    def execute(self):
        # create a thread pool executor
        n = multiprocessing.cpu_count()
        executor = ThreadPoolExecutor(n*16)

        # Execute nodes until there is no more nodes to calculate and no nodes in calculation.
        while self.shouldStillRun():
            if not self.done_tasks.empty():
                node = self.done_tasks.get()
                self.lock.acquire()
                # Add the nodes that follow in the graph to the to calculate list and remove self from active nodes.
                self.toCalculate.extend(node.nextNodes)
                if node in self.activeCalculations:
                    self.activeCalculations.remove(node)
                if node.isRepeating():
                    self.toCalculate.append(node)
                self.lock.release()
                self.done_tasks.task_done()
                continue

            # When there are only active calculations and nothing new, wait.
            if not self.toCalculate:
                time.sleep(0.01)
                continue

            self.lock.acquire()
            # Select the node to execute and check if it can be executed.
            node = self.toCalculate[0]
            self.toCalculate = [value for value in self.toCalculate if value != node]
            if node in self.activeCalculations:
                self.toCalculate.append(node)
                self.lock.release()
                continue
            
            # Check if node needs main thread if so cannot be started in this thread.    
            if node.needsForeground():
                self.toCalculateMainThread.append(node)
                self.lock.release()
                continue
                
            if self.checkIfReady(node):
                # Prepare the input value set for the node.
                abort = False
                for key in node.inputBuffer:
                    if node.inputBuffer[key] is None:
                        abort = True
                        break

                if not abort:
                    # Add the node to the active calculations list and start a calculation thread.
                    self.activeCalculations.append(node)
                    executor.submit(self.executeNode, node, node.inputBuffer)
            self.lock.release()


    def executeNode(self, node, value):
        # Tick the node and then add the result to calculated.
        result = node.tick(value)

        for key in node.outs:
            for elem in node.outs[key]:
                resultNode = elem["node"]
                resultNode.inputBuffer[elem["var"]] = result[key]
                if "tags" in result and key in result["tags"]:
                    resultNode.inputBuffer["tags"][elem["var"]] = result["tags"][key]
                #print(resultNode.inputBuffer)
        self.done_tasks.put(node)

    def shouldStillRun(self):
        self.lock.acquire()
        should_run = (self.toCalculate or self.toCalculateMainThread or self.activeCalculations) and not builtins.registry["kill"]
        self.lock.release()
        return should_run

    def checkIfReady(self, node):
        # Check if all nodes are calculated.
        for key in node.ins:
            if key not in node.inputBuffer:
                return False
        return True

if __name__ == "__main__":
    # Execute all graph paths passed as parameters.
    if len(sys.argv) < 2:
        print("Usage: Pass graph json files to execute as parameters.")
    else:
        offset = 2
        if len(sys.argv) > offset and sys.argv[offset] == "debug":
            builtins.registry["debugger"] = debugger.Debugger()
            offset += 1
        if len(sys.argv) > offset:
            builtins.registry = json.loads(" ".join(sys.argv[offset:]))
        builtins.registry["kill"] = False
        gex = GraphEx(sys.argv[1])
        gex.prepareExecution()
        gex.executeThreaded()
        for hook in builtins.shutdown_hook:
            hook()
        print(json.dumps(builtins.registry_output))
