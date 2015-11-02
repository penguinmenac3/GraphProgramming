var WebUI = new WebUI_CWebUI();

function WebUI_CWebUI() {
	var that = this;
	var KeyListener = null;
	var RenderEngine = null;
	this.keyboard_input_state = true;
	this.mouse_click_listener = null;
	this.debug = false;
	this.graph = null;
	this.nodes = null;
	this.selectedNode = null;
	that.graphName = "Default";
	this.selectedConnection = null;
	that.startPos = null;
	
	this.start = function(fullscreen, width, height, container) {
		/* check if dependencies are already existing */
		if (KeyListener == null && RenderEngine == null) {
			KeyListener = new WebUI_CKeyListener();
			RenderEngine = new WebUI_CRenderEngine();
		} else {
			return false; /* an error occured, there is already running a web ui on this tab. */
		}

		/* init the RenderEngine */
		var canvas = RenderEngine.init(fullscreen, width, height, container);
		RenderEngine.render(60);
		/* init the ObjectManager, needs canvas for MouseHandlers */
		KeyListener.init(canvas);
		/* start the render loop with the key listener */
		KeyListener.launch(RenderEngine);

		getGraph(that.graphName, that.setGraph, that.printError);
		getNodes("PythonNodes", that.setNodes, that.printError);
		return true;
	};

	this.setGraph = function(graph) {
		that.graph = graph;
	};

	this.setNodes = function(nodes) {
		that.nodes = nodes;
		console.log(nodes);
	};

	this.saveGraph = function(name) {
		setGraph(name, that.graph, that.savedGraph, that.printError);
	};

	this.savedGraph = function(success) {
		console.log(success);
	};

	this.printError = function(text) {
		console.log(text);
	};

	this.trySelect = function(x, y) {		
		absX = x + RenderEngine.getOffsetX() + RenderEngine.getSize().width / 2;
		absY = y + RenderEngine.getOffsetY() + RenderEngine.getSize().height / 2;
		if (absX > 10 && absX < 90) {
			if (absY > 10 && absY < 40) {
				name = prompt("Please enter graph name", WebUI.graphName);
				if (name == null) {
					return;
				}
				WebUI.graphName = name;
				getGraph(WebUI.graphName, WebUI.setGraph, WebUI.printError);
				return;
			}
			if (absY > 50 && absY < 80) {
				name = prompt("Please enter graph name", WebUI.graphName);
				if (name == null) {
					return;
				}
				WebUI.saveGraph(name);
				return;
			}
			if (absY > 90 && absY < 120) {
				name = prompt("Please enter node spec name", "PythonNodes");
				if (name == null) {
					return;
				}
				getNodes(name, that.setNodes, that.printError);
				return;
			}
			if (absY > 130 && absY < 160) {
				classes = "";
				that.nodes.forEach(function(node) {
					classes += node.code + ",";
				});
				nodeclass = prompt("Node Class ["+classes + "]", null);
				if (nodeclass == null) {
					return;
				}
				selectedNode = null;
				that.nodes.forEach(function(node) {
					if (node.code == nodeclass) {
						selectedNode = node;
					}
				});
				if (selectedNode == null) {
					return;
				}
				nodename = prompt("Node Name (must be unique)", selectedNode.name);
				if (nodename == null) {
					return;
				}
				selectedNode = JSON.parse(JSON.stringify(selectedNode));
				selectedNode.name = nodename;
				graph.nodes.push(selectedNode);

				return;
			}
			if (absY > 170 && absY < 200) {
				alert("Drop a node here to delete it.");
				return;
			}
		}
		that.startPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};

		graph.nodes.forEach(function(node) {
			x1 = node.x - RenderEngine.nodeWidth/2;
			y1 = node.y - RenderEngine.nodeHeight/2;
			x2 = node.x - RenderEngine.nodeWidth/2 + RenderEngine.dotSize;
			y2 = node.y - RenderEngine.nodeHeight/2 + RenderEngine.dotSize;
			if (x > x1 && x < x2 && y > y1 && y < y2) {
				that.selectedNode = node;
				return;
			}
		});
		graph.nodes.forEach(function(node) {
			input = tryFindInput(node, x, y);
			if (input != null) {
				that.selectedNode = node;
				that.selectedInputConnection = input;
				updateGraph(that.selectedNode, null, that.selectedInputConnection, null);
				return;
			}
			output = tryFindOutput(node, x, y);
			if (output != null) {
				that.selectedNode = node;
				that.selectedOutputConnection = output;
				updateGraph(null, that.selectedNode, null, that.selectedOutputConnection);
				return;
			}
		});
	};

	function tryFindInput(node, x, y) {
		var result = null;
		for (var connection in node.inputs) {
  			if (node.inputs.hasOwnProperty(connection)) {
				pos = RenderEngine.getNodeInputPosition(that.graph, node.name, connection);
				x1 = pos.x - RenderEngine.dotSize/2;
				y1 = pos.y - RenderEngine.dotSize/2;
				x2 = pos.x + RenderEngine.dotSize/2;
				y2 = pos.y + RenderEngine.dotSize/2;
				if (x > x1 && x < x2 && y > y1 && y < y2) {
					result = connection;
					console.log(node);
					return connection;
				}
			}
		}
		return result;
	}

	function tryFindOutput(node, x, y) {
		var result = null;
		for (var connection in node.outputs) {
  			if (node.outputs.hasOwnProperty(connection)) {
				pos = RenderEngine.getNodeOutputPosition(that.graph, node.name, connection);
				x1 = pos.x - RenderEngine.dotSize/2;
				y1 = pos.y - RenderEngine.dotSize/2;
				x2 = pos.x + RenderEngine.dotSize/2;
				y2 = pos.y + RenderEngine.dotSize/2;
				if (x > x1 && x < x2 && y > y1 && y < y2) {
					result = connection;
					console.log(node);
					return connection;
				}
			}
		}
		return result;
	}

	this.moveSelected = function(x, y) {
		absX = x + RenderEngine.getOffsetX() + RenderEngine.getSize().width / 2;
		absY = y + RenderEngine.getOffsetY() + RenderEngine.getSize().height / 2;
		if (that.selectedInputConnection != null) {
			pos = RenderEngine.getNodeInputPosition(that.graph, that.selectedNode.name, that.selectedInputConnection);
			RenderEngine.tmpNodeLine(pos.x, pos.y, x, y);
		} else if (that.selectedOutputConnection != null) {
			pos = RenderEngine.getNodeOutputPosition(that.graph, that.selectedNode.name, that.selectedOutputConnection);
			RenderEngine.tmpNodeLine(pos.x, pos.y, x, y);
		} else if (that.selectedNode != null) {
			that.selectedNode.x = x + RenderEngine.nodeWidth/2 - RenderEngine.dotSize / 2;
			that.selectedNode.y = y + RenderEngine.nodeHeight/2 - RenderEngine.dotSize / 2;
		} else if (that.startPos != null) {
			nextPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};
			RenderEngine.move(nextPos.x - that.startPos.x, nextPos.y - that.startPos.y);
			that.startPos = nextPos;
		}
	};

	this.unselect = function(x, y) {
		absX = x + RenderEngine.getOffsetX() + RenderEngine.getSize().width / 2;
		absY = y + RenderEngine.getOffsetY() + RenderEngine.getSize().height / 2;
		if (that.selectedInputConnection != null) {
			outputName = null;
			outputNode = null;
			graph.nodes.forEach(function(node) {
				output = tryFindOutput(node, x, y);
				if (output != null) {
					outputName = output;
					outputNode = node;
					return;
				}
			});
			updateGraph(that.selectedNode, outputNode, that.selectedInputConnection, outputName);
			RenderEngine.removeTmpNodeLine();
			that.selectedInputConnection = null;
			that.selectedNode = null;
		} else if (that.selectedOutputConnection != null) {
			inputName = null;
			inputNode = null;
			graph.nodes.forEach(function(node) {
				input = tryFindInput(node, x, y);
				if (input != null) {
					inputName = input;
					inputNode = node;
					return;
				}
			});
			updateGraph(inputNode, that.selectedNode, inputName, that.selectedOutputConnection);
			RenderEngine.removeTmpNodeLine();
			that.selectedOutputConnection = null;
			that.selectedNode = null;
		} else if (that.selectedNode != null) {
			that.selectedNode.x = x + RenderEngine.nodeWidth/2 - RenderEngine.dotSize / 2;
			that.selectedNode.y = y + RenderEngine.nodeHeight/2 - RenderEngine.dotSize / 2;

			if (absX > 10 && absX < 90 && absY > 170 && absY < 200) {
				for (var connection in that.selectedNode.inputs) {
  					if (that.selectedNode.inputs.hasOwnProperty(connection)) {
						updateGraph(that.selectedNode, null, connection, null);
					}
				}
				for (var connection in that.selectedNode.outputs) {
  					if (that.selectedNode.outputs.hasOwnProperty(connection)) {
						updateGraph(null, that.selectedNode, null, connection);
					}
				}
				var index = graph.nodes.indexOf(that.selectedNode);
    			graph.nodes.splice(index, 1);
				return;
			}
			that.selectedNode = null;
		} else if (that.startPos != null) {
			nextPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};
			RenderEngine.move(nextPos.x - that.startPos.x, nextPos.y - that.startPos.y);
			that.startPos = null;
		}
	};

	function updateGraph(inputNode, outputNode, inputName, outputName) {
		toRemove = null;
		graph.connections.forEach(function(connection) {
			if (inputNode != null && connection.output.node == inputNode.name && connection.output.input == inputName) {
				toRemove = connection;
			}
		});
		if (toRemove != null) {
			var index = graph.connections.indexOf(toRemove);
    		graph.connections.splice(index, 1);
		}
		toRemove = null;
		graph.connections.forEach(function(connection) {
			if (outputNode != null && connection.input.node == outputNode.name && connection.input.output == outputName) {
				toRemove = connection;
			}
		});
		if (toRemove != null) {
			var index = graph.connections.indexOf(toRemove);
    		graph.connections.splice(index, 1);
		}

		if (inputNode != null && outputNode != null && inputName != null && outputName != null) {
			graph.connections.push({"input":{"node":outputNode.name, "output": outputName}, "output":{"node":inputNode.name, "input": inputName}});
		}
	}
}