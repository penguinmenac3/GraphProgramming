var WebUI = new WebUI_CWebUI();

function WebUI_CWebUI() {
	var that = this;
	var KeyListener = null;
	var RenderEngine = null;
    var moved = false;
    var moveOffsetX = 0;
    var moveOffsetY = 0;
    var codeMirror = null;
    var codeTheme = "default";
    this.currentNode = null;
	this.keyboard_input_state = true;
	this.mouse_click_listener = null;
	this.debug = false;
	this.graph = null;
    this.graphStack = new Array();
    this.graphNameStack = new Array();
	this.nodes = null;
	this.selectedNode = null;
	this.graphName = "Default";
	this.selectedConnection = null;
	this.startPos = null;
	this.clickNode = null;
	
	this.start = function(fullscreen, container, initialGraph) {
		/* check if dependencies are already existing */
		if (KeyListener == null && RenderEngine == null) {
			KeyListener = new WebUI_CKeyListener();
			RenderEngine = new WebUI_CRenderEngine();
		} else {
			return false; /* an error occured, there is already running a web ui on this tab. */
		}
        that.graphName = initialGraph;

		/* init the RenderEngine */
		var canvas = RenderEngine.init(fullscreen, container);
		RenderEngine.render(60);
		/* init the ObjectManager, needs canvas for MouseHandlers */
		KeyListener.init(canvas);
		/* start the render loop with the key listener */
		KeyListener.launch(RenderEngine);

        RenderEngine.setHasParent(false);
		getGraph(that.graphName, that.setGraph, that.printError);
		getNodes("Python", that.setNodes, that.printError);
        showInfo();
		return true;
	};
    
    this.setTheme = function(theme) {
        that.theme = theme;
        if (theme == "dark") {
            RenderEngine.setTheme("#333333", "green", "#D75813", "darkslategray", "#AB0000", "rgba(150,150,150,0.6)", "darkgray", "#AB0000");
            codeTheme = "lesser-dark";
        } else if (theme == "light") {    
            RenderEngine.setTheme("white", "#3CB371", "orange", "darkslategray", "indianred", "rgba(128,128,128,0.6)", "rgb(128,128,128)", "red");
            codeTheme = "default";
        }
    }

	this.setGraph = function(graph) {
        that.graphStack.push(graph);
        that.graphNameStack.push(that.graphName);
		that.graph = graph;
        localStorage.graph = that.graphName;
        if (that.graphStack.length > 1) {
            RenderEngine.setHasParent(true);
        }
        RenderEngine.setDirty();
		that.changed = false;
	};

	this.setNodes = function(nodes) {
		that.nodes = nodes;
	};

	this.saveGraph = function(name) {
		setGraph(name, that.graph, that.savedGraph, that.printError);
	};

	this.savedGraph = function(success) {
		console.log(success);
	};

	this.printError = function(text) {
        document.getElementById("erroroverlay").style.display = "";
        document.getElementById("innererroroverlay").innerHTML = '<h2>An Error Occured</h2>' + text;
		console.log(text);
	};
    
	this.printErrorTitled = function(title, text) {
        document.getElementById("erroroverlay").style.display = "";
        document.getElementById("innererroroverlay").innerHTML = '<h2>' + title + '</h2>' + text;
	};
    function makeid() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i=0; i < 5; i++ )
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }

    this.createNode = function(nodeclass) {
				if (nodeclass == null) {
					return;
				}
                
                that.hideNodeSelector();
				var selectedNode = null;
				that.nodes.forEach(function(node) {
					if (node.code == nodeclass) {
						selectedNode = node;
					}
				});
				if (selectedNode == null) {
					return;
				}
				var nodename = prompt("Node Name", selectedNode.name);
				if (nodename == null) {
					return;
				}
				selectedNode = JSON.parse(JSON.stringify(selectedNode));
				selectedNode.name = makeid();
                selectedNode.displayname = nodename;
				graph.nodes.push(selectedNode);
                RenderEngine.setDirty();

				that.changed = true;
    };
    
    this.hideNodeSelector = function() {
        document.getElementById("nodeselector").style.display = "none";
    };
    
    this.changeLanguage = function(language) {
        that.hideLanguageSelector();
        getNodes(language, that.setNodes, WebUI.printError);
    };
    this.hideLanguageSelector = function() {
        document.getElementById("languageselector").style.display = "none";
    };
    
    this.hideErrorOverlay = function() {
        document.getElementById("erroroverlay").style.display = "none";
    };
    
    this.hideCodeEditor = function() {
        document.getElementById("codeeditor").style.display = "none";
    };

	this.trySelect = function(x, y) {		
        var scale = RenderEngine.getScale();
		var absX = x + RenderEngine.getOffsetX() * scale + RenderEngine.getSize().width / 2;
		var absY = y + RenderEngine.getOffsetY() * scale + RenderEngine.getSize().height / 2;
        var canvasSize = RenderEngine.getSize();
        if (absX < canvasSize.width - 10 && absX > canvasSize.width - 90) {
            if (absY > 10 && absY < 40) {
				RenderEngine.changeScale(-0.2);
				return;
			}
			if (absY > 50 && absY < 80) {
				RenderEngine.changeScale(0.2);
				return;
			}
            if (absY > 90 && absY < 120) {
                RenderEngine.resetScale();
                return;
            }
            if (absY > 130 && absY < 160) {
                RenderEngine.resetScale();
                RenderEngine.resetOffset();
                return;
            }
            if (absY > RenderEngine.getSize().height / 2 - 15 && absY < RenderEngine.getSize().height / 2 + 15) {
                if (RenderEngine.showInfo) {
                    showInfo();
                } else {
                    RenderEngine.showInfo = true;
                    document.getElementById("graphview").style.right = "0";
                    document.getElementById("infocontent").innerHTML = "Click/Tap on a node to show info about it.";
                    that.currentNode = null;
                    RenderEngine.marked = null;
                }
                RenderEngine.resize();
                RenderEngine.setDirty();
                return;
            }
        }
		if (absX > 10 && absX < 90) {
			if (absY > 10 && absY < 40) {
				var name = prompt("Please enter graph name", WebUI.graphName);
				if (name == null) {
					return;
				}
				WebUI.graphName = name;
                that.graphStack = new Array();
                that.graphNameStack = new Array();
                RenderEngine.setHasParent(false);
				getGraph(WebUI.graphName, WebUI.setGraph, WebUI.printError);
				return;
			}
			if (absY > 50 && absY < 80) {
				if (that.changed == true) {
					var name = prompt("Save: Please enter graph name", WebUI.graphName);
					if (name == null) {
						console.log("Abortion");
						return;
					}
					WebUI.graphName = name;
					WebUI.saveGraph(WebUI.graphName);
					that.changed = false;
				}
				return;
			}
			if (absY > 90 && absY < 120) {
                document.getElementById("languageselector").style.display = "";
				return;
			}
			if (absY > 130 && absY < 160) {
				var classes = {};
				that.nodes.forEach(function(node) {
                    var nodetype = "algorithmnode";
                    if (Object.keys(node.inputs).length == 0) {
                        nodetype = "inputnode";
                    } else if (Object.keys(node.outputs).length == 0) {
                        nodetype = "outputnode";
                    } else if (node.code.lastIndexOf("structures", 0) === 0 || (node.code.lastIndexOf("default", 0) === 0 && node.code.lastIndexOf("function", "default.".length) < 0)) {
                        nodetype = "structurenode";
                    }
                    var cur = node.code.split(".")[0];
                    if (!classes[cur]) {
                        prefix = cur;
                        classes[cur] = "<h2>" + prefix.toUpperCase() + "</h2>";
                    }
					classes[cur] += '<button onclick="WebUI.createNode(\'' + node.code + '\')" class="node ' + nodetype + '">' + node.name + '</button>';
				});
                var classesStr = "";
                var keys = [];
                for (var key in classes) {
                    if (classes.hasOwnProperty(key)) {
                        keys.push(key);
                    }
                }
                keys = keys.sort();
                classesStr += classes["default"];
                classesStr += classes["structures"];
                for (var key in keys) {
                    if (keys[key] == "structures" || keys[key] == "default") {
                        continue;
                    }
                    classesStr += classes[keys[key]];
                }
                document.getElementById("innernodeselector").innerHTML = classesStr;
                document.getElementById("nodeselector").style.display = "";
				return;
			}
			if (absY > 170 && absY < 200) {
                that.printErrorTitled("Hint","Drop a node here to delete it.");
				return;
			}
			/*if (absY > 210 && absY < 240) {
				if (that.changed == true) {
					var name = prompt("Autosave: Please enter graph name", WebUI.graphName);
					if (name == null) {
						return;
					}
					WebUI.graphName = name;
					WebUI.saveGraph(WebUI.graphName);
					that.changed = false;
				}
				execute(that.graphName, RenderEngine.setResult, RenderEngine.setResult);
				return;
			}*/
			if (absY > 250 && absY < 280) {
				if (that.changed == true) {
					var name = prompt("Autosave: Please enter graph name", WebUI.graphName);
					if (name == null) {
						return;
					}
					WebUI.graphName = name;
					WebUI.saveGraph(WebUI.graphName);
					that.changed = false;
				}
				start(that.graphName, that.setDebug, that.setDebug);
				return;
			}
			if (absY > 290 && absY < 310) {
				kill();
				return;
			}
			if (absY > 370 && absY < 390) {
                if (that.graphStack.length < 2) {
                    return;
                }
				if (that.changed == true) {
					that.graphName = name;
					that.saveGraph(that.graphName);
				}
                that.graphStack.pop();
                that.graphNameStack.pop();
                that.graph = that.graphStack[that.graphStack.length-1];
                that.graphName = that.graphNameStack[that.graphNameStack.length-1];
                if (that.graphStack.length < 2) {
                    RenderEngine.setHasParent(false);
                }
                RenderEngine.setDirty();
				return;
			}
		}

		that.startPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};

		graph.nodes.forEach(function(node) {
			var x1 = node.x * scale - RenderEngine.nodeWidth/2 * scale;
			var y1 = node.y * scale - RenderEngine.nodeHeight/2 * scale;
			var x2 = node.x * scale + RenderEngine.nodeWidth/2 * scale;
			var y2 = node.y * scale + RenderEngine.nodeHeight/2 * scale;
			if (x > x1 && x < x2 && y > y1 && y < y2) {
				that.selectedNode = node;
                moveOffsetX = node.x - x;
                moveOffsetY = node.y - y;
                moved = false;
				return;
			}
			var input = tryFindInput(node, x, y);
			if (input != null) {
				that.selectedNode = node;
				that.selectedInputConnection = input;
				updateGraph(that.selectedNode, null, that.selectedInputConnection, null);
				return;
			}
			var output = tryFindOutput(node, x, y);
			if (output != null) {
				that.selectedNode = node;
				that.selectedOutputConnection = output;
				updateGraph(null, that.selectedNode, null, that.selectedOutputConnection);
				return;
			}
		});
	};
    
    this.deselectNode = function () {
        document.getElementById("infocontent").innerHTML = "Click/Tap on a node to show info about it.";
        RenderEngine.marked = null;
        that.currentNode = null;
        RenderEngine.setDirty();
    }
    
    this.nodeChanged = function () {
        if (document.getElementById("args")) {
            that.currentNode.args = JSON.parse(document.getElementById("args").value);
        }
        if ((typeof that.currentNode.args) == "object") {
            for (var property in that.currentNode.args) {
                if (that.currentNode.args.hasOwnProperty(property)) {
                    
                    if (property == "code") {
                        // Do nothing, is only changed via editor.
                    } else {
                        elemId = "args-" + property;
                        that.currentNode.args[property] = JSON.parse(document.getElementById(elemId).value);
                    }
                }
            }
        }
        
        that.currentNode.desc = document.getElementById("desc").value;
        that.currentNode.displayname = document.getElementById("displayname").value;
	    that.changed = true;
        RenderEngine.setDirty();
    }
    
    this.saveCodeEdit = function (property) {
        codeMirror.toTextArea();
        that.currentNode.args[property] = document.getElementById("src").value;
        that.changed = true;
        RenderEngine.setDirty();
        WebUI.hideCodeEditor();
    }
    
    this.saveCodePeek = function(property) {
        codeMirror.toTextArea();
        src = document.getElementById("src").value;
        setSrc(property, src, that.printError);
        WebUI.hideCodeEditor();
    }
    
    this.codeEdit = function(property) {
        var src = that.currentNode.args[property];
        
        var srcEdit = "<textarea id='src' class='src'>" + src + "</textarea>";
        var savebtn = "<button class='node inputnode right' onclick='WebUI.saveCodeEdit(\""+property+"\")'>Save</button>";
        var cancelbtn = "<button class='node outputnode right' onclick='WebUI.hideCodeEditor()'>Cancel</button>"
        
        var nname = that.currentNode.displayname;
        
        document.getElementById("codeeditor").style.display = "";
        document.getElementById("innercodeeditor").innerHTML = '<h2>' + nname + ".args." + property + '</h2>' + srcEdit + cancelbtn + savebtn;
        codeMirror = CodeMirror.fromTextArea(document.getElementById("src"), {lineNumbers: true, theme: codeTheme});
    }
    
    function showCode(src) {
        var srcEdit = "<textarea id='src' class='src'>" + src + "</textarea>";
        var savebtn = "<button class='node inputnode right' onclick='WebUI.saveCodePeek(\"" + that.currentNode.code + "\")'>Save</button>";
        if (localStorage.devmode != "true") {
            savebtn = "";
            srcEdit = "<textarea id='src' class='src' readonly>" + src + "</textarea>";
        }
        var cancelbtn = "<button class='node outputnode right' onclick='WebUI.hideCodeEditor()'>Cancel</button>"
        
        var nname = that.currentNode.displayname;
        
        document.getElementById("codeeditor").style.display = "";
        document.getElementById("innercodeeditor").innerHTML = '<h2>' + that.currentNode.code + '</h2>' + srcEdit + cancelbtn + savebtn;
        codeMirror = CodeMirror.fromTextArea(document.getElementById("src"), {lineNumbers: true, theme: codeTheme});
    }
    
    
    this.codePeek = function(property) {
        showCode("Downloading code.");
        getSrc(property, showCode, that.printError);
    }

	function tryFindInput(node, x, y) {
        var scale = RenderEngine.getScale();
		var result = null;
		for (var connection in node.inputs) {
  			if (node.inputs.hasOwnProperty(connection)) {
				var pos = RenderEngine.getNodeInputPosition(that.graph, node.name, connection);
				var x1 = pos.x * scale - RenderEngine.dotTouchSize/2 * scale;
				var y1 = pos.y * scale - RenderEngine.dotTouchSize/2 * scale;
				var x2 = pos.x * scale + RenderEngine.dotTouchSize/2 * scale;
				var y2 = pos.y * scale + RenderEngine.dotTouchSize/2 * scale;
				if (x > x1 && x < x2 && y > y1 && y < y2) {
					var result = connection;
					return connection;
				}
			}
		}
		return result;
	}

	function tryFindOutput(node, x, y) {
        var scale = RenderEngine.getScale();
		var result = null;
		for (var connection in node.outputs) {
  			if (node.outputs.hasOwnProperty(connection)) {
				var pos = RenderEngine.getNodeOutputPosition(that.graph, node.name, connection);
				var x1 = pos.x * scale - RenderEngine.dotTouchSize/2 * scale;
				var y1 = pos.y * scale - RenderEngine.dotTouchSize/2 * scale;
				var x2 = pos.x * scale + RenderEngine.dotTouchSize/2 * scale;
				var y2 = pos.y * scale + RenderEngine.dotTouchSize/2 * scale;
				if (x > x1 && x < x2 && y > y1 && y < y2) {
					var result = connection;
					return connection;
				}
			}
		}
		return result;
	}

	this.moveSelected = function(x, y) {
        var scale = RenderEngine.getScale();
		var absX = x + RenderEngine.getOffsetX() + RenderEngine.getSize().width / 2;
		var absY = y + RenderEngine.getOffsetY() + RenderEngine.getSize().height / 2;
		if (that.selectedInputConnection != null) {
			var pos = RenderEngine.getNodeInputPosition(that.graph, that.selectedNode.name, that.selectedInputConnection);
			RenderEngine.tmpNodeLine(pos.x, pos.y, x / scale, y / scale);
		} else if (that.selectedOutputConnection != null) {
			var pos = RenderEngine.getNodeOutputPosition(that.graph, that.selectedNode.name, that.selectedOutputConnection);
			RenderEngine.tmpNodeLine(pos.x, pos.y, x / scale, y / scale);
		} else if (that.selectedNode != null) {
			that.selectedNode.x = x / scale + moveOffsetX;
			that.selectedNode.y = y / scale + moveOffsetY;
            moved = true;
            RenderEngine.setDirty();
		} else if (that.startPos != null) {
			var nextPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};
			RenderEngine.move(nextPos.x - that.startPos.x, nextPos.y - that.startPos.y);
			that.startPos = nextPos;
		}
	};

	this.unselect = function(x, y) {
        var scale = RenderEngine.getScale();
		var absX = x + RenderEngine.getOffsetX() + RenderEngine.getSize().width / 2;
		var absY = y + RenderEngine.getOffsetY() + RenderEngine.getSize().height / 2;
		var spos = that.startPos;
		that.startPos = null;
		if (that.selectedInputConnection != null) {
			var outputName = null;
			var outputNode = null;
			graph.nodes.forEach(function(node) {
				var output = tryFindOutput(node, x, y);
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
			that.changed = true;
            RenderEngine.setDirty();
		} else if (that.selectedOutputConnection != null) {
			var inputName = null;
			var inputNode = null;
			graph.nodes.forEach(function(node) {
				var input = tryFindInput(node, x, y);
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
			that.changed = true;
            RenderEngine.setDirty();
		} else if (that.selectedNode != null) {
            if (!moved) {
                that.currentNode = that.selectedNode;
				that.clickNode = null;
				that.startPos = null;
                var html = "";
                var nname = that.currentNode.displayname;
                html += "<h3><input class='hinput' id='displayname' value='" + nname + "' /></h3>";
                //console.log(currentNode);
                html += "<h4>Code</h4><p>" + that.currentNode.code + "<button class='button algorithmnode right' onclick='WebUI.codePeek(\"" + that.currentNode.code + "\")'>Peek</button></p>";
                html += "<h4>Desc</h4><p><input class='pinput' id='desc' value='" + that.currentNode.desc + "' /></p>";
                
                html += "<h4>Inputs</h4><p>"
                for (var property in that.currentNode.inputs) {
                    if (that.currentNode.inputs.hasOwnProperty(property)) {
                        html += "" + property + ": " + JSON.stringify(that.currentNode.inputs[property]) + "<BR>";
                    }
                }
                html += "</p>";
                html += "<h4>Outputs</h4><p>"
                for (var property in that.currentNode.outputs) {
                    if (that.currentNode.outputs.hasOwnProperty(property)) {
                        html += "" + property + ": " + JSON.stringify(that.currentNode.outputs[property]) + "<BR>";
                    }
                }
                html += "</p>";
                
                var iteratable = false;
                if ((typeof that.currentNode.args) == "object") {
                for (var property in that.currentNode.args) {
                    if (that.currentNode.args.hasOwnProperty(property)) {
                        if (iteratable == false) {
                            html += "<h4>Args</h4><p>"
                        }
                        if (property == "code") {
                            html += "" + property + ": <button class='button algorithmnode right' onclick='WebUI.codeEdit(\""+property+"\")'>Edit</button><BR>";
                        } else {
                            html += "" + property + ": <input class='pinput' id='args-" + property + "' value='" + JSON.stringify(that.currentNode.args[property]) + "' /><BR>";
                        }
                        iteratable = true;
                    }
                }
                }
                if (iteratable == false) {
                    html += "<h4>Args</h4><p><input class='pinput' id='args' value='" + JSON.stringify(that.currentNode.args) + "' /></p>";
                } else {
                    html += "</p>"
                }
                if(that.currentNode.code == "system.subgraph") {
				    html += "<p><button class='node algorithmnode right' onclick='getGraph(\"" + that.currentNode.args + "\", WebUI.setGraph, WebUI.printError)'>Edit Subgraph</button><p>";
                }
                html += "<p style='padding-top:1em'><button class='button inputnode' onclick='WebUI.nodeChanged()'>Save</button>";
                html += "<button class='button outputnode' onclick='WebUI.deselectNode()'>Unselect</button></p>";
                document.getElementById("infocontent").innerHTML = html;
                RenderEngine.marked = that.currentNode;
                showInfo();
                RenderEngine.setDirty();
			} else {
			    that.selectedNode.x = x / scale + moveOffsetX;
		    	that.selectedNode.y = y / scale + moveOffsetY;
                RenderEngine.setDirty();

			    if (absX > 10 && absX < 90 && absY > 170 && absY < 200) {
			    	for (var connection in that.selectedNode.inputs) {
  			    		if (that.selectedNode.inputs.hasOwnProperty(connection)) {
			    			updateGraph(that.selectedNode, null, connection, null, true);
			    		}
			    	}
			    	for (var connection in that.selectedNode.outputs) {
  			    		if (that.selectedNode.outputs.hasOwnProperty(connection)) {
			    			updateGraph(null, that.selectedNode, null, connection, true);
			    		}
			    	}
			    	var index = graph.nodes.indexOf(that.selectedNode);
    		    	graph.nodes.splice(index, 1);

    				that.changed = true;
    				return;
    			}
            }
			that.selectedNode = null;
			that.changed = true;
		} else if (spos != null) {
			var nextPos = {"x":x+RenderEngine.getOffsetX(), "y":y+RenderEngine.getOffsetY()};
			RenderEngine.move(nextPos.x - spos.x, nextPos.y - spos.y);
		}
	};

	function updateGraph(inputNode, outputNode, inputName, outputName, force) {
		force = typeof force !== 'undefined' ? force : false;
		var toRemove = [];
		graph.connections.forEach(function(connection) {
			if (inputNode != null && connection.output.node == inputNode.name && connection.output.input == inputName) {
				var allowedToRemove = true;
				if (force == false) {
					that.nodes.forEach(function(node) {
						if (node.code == inputNode.code) {
							if(node.loopback != null && (node.loopback.indexOf(inputName) > -1)) {
								allowedToRemove = false;
							}
						}
					});
				}
				if (allowedToRemove == true) {
					toRemove.push(connection);
				}
			}
		});
		graph.connections.forEach(function(connection) {
			if (outputNode != null && connection.input.node == outputNode.name && connection.input.output == outputName) {
				toRemove.push(connection);
			}
		});
		toRemove.forEach(function(elem) {
			var index = graph.connections.indexOf(elem);
    		graph.connections.splice(index, 1);
		});

		if (inputNode != null && outputNode != null && inputName != null && outputName != null) {
			graph.connections.push({"input":{"node":outputNode.name, "output": outputName}, "output":{"node":inputNode.name, "input": inputName}});
		}
        RenderEngine.setDirty();
	}
    
    function showInfo() {
        RenderEngine.showInfo = false;
        document.getElementById("graphview").style.right = "18em";
        RenderEngine.resize();
        RenderEngine.setDirty();
    }
    
    var lastDebug = "";
    this.setDebug = function (result) {
        if (lastDebug == result) {
            return;
        }
        lastDebug = result;
        showInfo();
        result = result.replace(new RegExp("\n", 'g'), "<br>");
        document.getElementById("debugcontent").innerHTML = "<button class='button outputnode right' onclick='WebUI.clearDebug()'>clear</button><br>" + result;
    }
    
    this.clearDebug = function () {
        lastDebug = "";
        document.getElementById("debugcontent").innerHTML = "Run graph to get debug output.";
    }
}
