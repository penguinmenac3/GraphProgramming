
function WebUI_CRenderEngine() {
    var containerDiv = null;
    var isDirty = 2;
	var that = this;
	var canvas = null;
	var ctx = null;
	var width = 0;
	var height = 0;
	var fullscreen = false;
	var renderOffsetX = 0;
	var renderOffsetY = 0;
    var scale = 1;
    var hasParent = false;
	this.dotSize = 20;
	this.nodeWidth = 200;
	this.nodeHeight = 80;
	this.tmpLine = null;
	this.result = "";
    this.showInfo = true;
    this.marked = null;
    
    this.setDirty = function() {
        isDirty = 2;
    };

	this.init = function(b_fullscreen, container) {
		fullscreen = b_fullscreen;
		/* create a canvas element */
		canvas = document.createElement('canvas');
		canvas.setAttribute('id', 'webuicontainer');
		/* bind it to the given container or the body */
		if (container == null) {
            containerDiv = document.body;
		} else {
            containerDiv = document.getElementById(container);
		}
		containerDiv.appendChild(canvas);
		/* fix the style to display it correctly */
		if (fullscreen) {
			canvas.style.position = "absolute";
		} else {
			canvas.style.position = "relative";
		}
		canvas.style.top = "0";
		canvas.style.left = "0";
		canvas.style.display = 'block';
		/* extract the context, that is required for rendering */
		ctx = canvas.getContext('2d');
		ctx.save();
		that.resize();
		window.onresize = function () {
			that.resize();
		};
		/*
		 * give back the canvas to give other classes the possibility to append
		 * InputListeners to it
		 */
		return canvas;
	};

	this.resize = function() {
		if (fullscreen == true) {
			//width = document.body.clientWidth - 1;
			width = window.innerWidth;
			height = window.innerHeight;
		} else {
			width = containerDiv.clientWidth;
			height = containerDiv.clientHeight;
		}
		canvas.width = width;
		canvas.height = height;
        that.setDirty();
	};

	this.move = function (dx, dy) {
		renderOffsetX += dx;
		renderOffsetY += dy;
        that.setDirty();
	};

	this.getOffsetX = function() {
		return renderOffsetX;
	};

	this.getOffsetY = function() {
		return renderOffsetY;
	};
    
    this.resetOffset = function() {
        renderOffsetX = 0;
        renderOffsetY = 0;
        that.setDirty();
    }

	this.getSize = function () {
		return {width:width, height:height};
	};
    
    this.changeScale = function(factor) {
        scale *= 1.0 + factor;
        that.setDirty();
    };
    
    this.resetScale = function() {
        scale = 1;
        that.setDirty();
    };
    
    this.getScale = function() {
        return scale;
    };
    
    this.setHasParent = function(hasParentParam) {
        hasParent = hasParentParam;
        that.setDirty();
    }

	/* switch fullscreen flag & change pos attr for correct positioning */
	this.toggleFullscreen = function() {
		if (fullscreen) {
			canvas.style.position = "relative";
			fullscreen = false;
		} else {
			canvas.style.position = "absolute";
			fullscreen = true;
		}
		that.resize();
	};
	/* force a certain fullscreen state */
	this.forceFullscreen = function(b_full) {
		if (b_full == true) {
			canvas.style.position = "absolute";
			fullscreen = true;
		} else {
			canvas.style.position = "relative";
			fullscreen = false;
		}
		resize();
	};

	this.getPartial = function() {
		var partial = data_width / width;
		if (partial < data_height / height) {
			partial = data_height / height;
		}
		return partial;
	};
	
	/* give out the absolute canvas position */
	this.getCanvasPosition = function() {
		var elem = canvas, tagname = "", x = 0, y = 0;
		while ((typeof (elem) == "object")
				&& (typeof (elem.tagName) != "undefined")) {
			y += elem.offsetTop;
			x += elem.offsetLeft;
			tagname = elem.tagName.toUpperCase();
			if (tagname == "BODY")
				elem = 0;
			if (typeof (elem) == "object")
				if (typeof (elem.offsetParent) == "object")
					elem = elem.offsetParent;
		}
		position = new Object();
		position.x = x;
		position.y = y;
		return position;
	};

	this.render = function(fps) {
        if (isDirty < 1) {
            return;
        }
        isDirty--;
		/* clean canvas */
        ctx.fillStyle = "white";
		ctx.fillRect(0, 0, width, height);

		/* Render the origin cross */
		ctx.beginPath();
		ctx.lineWidth="1";
		ctx.strokeStyle="red";
		ctx.moveTo(renderOffsetX * scale + width/2 - 20 * scale,renderOffsetY * scale + height/2);
		ctx.lineTo(renderOffsetX * scale + width/2 + 20 * scale,renderOffsetY * scale + height/2);
		ctx.moveTo(renderOffsetX * scale + width/2,renderOffsetY * scale + height/2 - 20 * scale);
		ctx.lineTo(renderOffsetX * scale + width/2,renderOffsetY * scale + height/2 + 20 * scale);
		ctx.stroke();


		/* rendering */
		if (that.tmpLine != null) {
			renderDotConnection(that.tmpLine.x1, that.tmpLine.y1, that.tmpLine.x2, that.tmpLine.y2);
		}
		renderGraph();
		renderActionButtons();

		/* Top pane */
		printResult()

		/* Bottom pane */
		ctx.font = "12px 'Helvetica'";
		ctx.fillStyle = "rgb(128,128,128)";
		ctx.textAlign = 'center';
		ctx.textBaseline = 'top';
		ctx.fillText("Implemented by Michael Fuerst 2015", width / 2, height - 15);

		/* Show fps when debug is enabled */
		if (WebUI.debug == true) {
			ctx.font = "10px 'Helvetica'";
			ctx.textAlign = 'center';
			ctx.textBaseline = 'top';
			if (fps > 60) {
				ctx.fillStyle = "rgb(0,255,255)";
			} else if (fps > 30) {
				ctx.fillStyle = "rgb(0,255,0)";
			} else if (fps > 15) {
				ctx.fillStyle = "rgb(255,255,0)";
			} else {
				ctx.fillStyle = "rgb(255,0,0)";
			}
			ctx.fillText("FPS: "+fps.toFixed(0), 30, 15);
		}
	};

	this.getNodePosition = function (graph, nodename) {
		node = that.findNode(graph, nodename);
		return {"x":node.x, "y":node.y}
	};

	this.getNodeInputPosition = function (graph, nodename, inputname) {
		node = that.findNode(graph, nodename);
		return getPosition(node, inputname, node.inputs, true);
	};

	this.getNodeOutputPosition = function (graph, nodename, outputname) {
		node = that.findNode(graph, nodename);
		return getPosition(node, outputname, node.outputs, false);
	};

	this.findNode = function(graph, name) {
		graph.nodes.forEach(function(node) {
			if (node.name == name) {
				result = node;
				return result;
			}
		});
		return result;
	};

	this.tmpNodeLine = function(x1,y1, x2, y2) {
		that.tmpLine = {"x1":x1, "x2":x2, "y1":y1, "y2": y2};
        that.setDirty();
	};

	this.removeTmpNodeLine = function() {
		that.tmpLine = null;
        that.setDirty();
	};

	/*this.setResult = function(text) {
		that.result = text;
        that.setDirty();
	};*/

	function renderDot(px, py, marked) {
		ctx.beginPath();
		ctx.lineWidth="1";
        if (!marked) {
		  ctx.strokeStyle="rgb(128,128,128)";
		  ctx.fillStyle = "rgb(244,244,244)";
        } else {
		  ctx.strokeStyle="rgb(128,200,128)";
		  ctx.fillStyle = "rgb(244,255,244)";
        }
		ctx.rect(renderOffsetX * scale + px * scale - that.dotSize/2 * scale + width/2,renderOffsetY * scale + py * scale - that.dotSize/2 * scale + height/2,that.dotSize * scale,that.dotSize * scale);
		ctx.fill();
		ctx.stroke();
	}

	function renderDotConnection(px1, py1, px2, py2) {
		ctx.beginPath();
		ctx.lineWidth="2";
		ctx.strokeStyle="rgb(128,128,128)";
		ctx.moveTo(renderOffsetX * scale + px1 * scale + width/2,renderOffsetY * scale + py1 * scale + height/2);
		ctx.lineTo(renderOffsetX * scale + px2 * scale + width/2,renderOffsetY * scale + py2 * scale + height/2);
		ctx.stroke();
	}

	function renderNodeText(text, x, y, offsetX, offsetY) {
		/* Write text with speed and curve info */
		ctx.font = parseInt(12 * scale) + "px 'Helvetica'";
		ctx.fillStyle = "rgb(128,128,128)";
		ctx.textAlign = 'center';
		ctx.textBaseline = 'center';
		ctx.fillText(text, renderOffsetX * scale + x * scale + width/2 + offsetX * scale, renderOffsetY * scale + y * scale + height/2 + offsetY * scale);
	}

	function renderNodeRect(x, y, marked) {
		ctx.beginPath();
		ctx.lineWidth="1";
        if (!marked) {
		  ctx.strokeStyle="rgb(128,128,128)";
		  ctx.fillStyle = "rgb(244,244,244)";
        } else {
		  ctx.strokeStyle="rgb(128,200,128)";
		  ctx.fillStyle = "rgb(244,255,244)";
        }
		ctx.rect(renderOffsetX * scale + x * scale + width/2-that.nodeWidth/2 * scale,renderOffsetY * scale + y * scale + height/2-that.nodeHeight/2 * scale,that.nodeWidth * scale,that.nodeHeight * scale);
		ctx.fill();
		ctx.stroke();
	}

	function renderGraph() {
		if (WebUI.graph != null) {
			graph = WebUI.graph;
			graph.connections.forEach(function(connection) {
				renderConnection(graph, connection);
			});
			graph.nodes.forEach(function(node) {
				renderNode(node);
			});
		}
	}

	function renderConnection(graph, connection) {
		pos1 = that.getNodeOutputPosition(graph, connection.input.node, connection.input.output);
		pos2 = that.getNodeInputPosition(graph, connection.output.node, connection.output.input);
		renderDotConnection(pos1.x, pos1.y, pos2.x, pos2.y);
	}

	function renderNode(node) {
		if (typeof node.x === "undefined" || typeof node.y === "undefined") {
			node.x = 0;
			node.y = 0;
			console.log("Default position for: " + node.name)
		}

		/* Draw rect symbol for robot */
		renderNodeRect(node.x, node.y, node == that.marked);

		/* Write text with speed and curve info */
        var nname = node.name;
        if (nname.lastIndexOf("_") != -1) {
            nname = nname.substring(0, nname.lastIndexOf("_"));
        }
		renderNodeText(nname, node.x, node.y, 0, -30);
		if (typeof node.args === "undefined") {
			node.args = {};
		}
		renderNodeText("args="+JSON.stringify(node.args), node.x, node.y, 0,  0);
		renderNodeText(node.desc, node.x, node.y, 0,  15);

		for (var key in node.inputs) {
  			if (node.inputs.hasOwnProperty(key)) {
  				pos = getPosition(node, key, node.inputs, true);
    			renderDot(pos.x, pos.y, node == that.marked);
  			}
		}
		for (var key in node.outputs) {
  			if (node.outputs.hasOwnProperty(key)) {
  				pos = getPosition(node, key, node.outputs, false);
    			renderDot(pos.x, pos.y, node == that.marked);
  			}
		}
		renderDot(node.x - that.nodeWidth/2 + that.dotSize / 2, node.y - that.nodeHeight/2 + that.dotSize / 2, node == that.marked);
	}

	function getPosition(parent, reference, list, isInput) {
		var len = 0;
		var i = 0;
		for (var key in list) {
  			if (list.hasOwnProperty(key)) {
    			len++;
  			}
		}
		for (var key in list) {
  			if (list.hasOwnProperty(key)) {
  				if (reference == key) {
  					dx = parent.x + ((i + 1.0) / (len + 1.0)) * that.nodeWidth - that.nodeWidth/2;
  					dy = parent.y;
  					if (isInput == true) {
  						dy -= that.nodeHeight/2 + that.dotSize / 2;
  					} else {
  						dy += that.nodeHeight/2 + that.dotSize / 2;
  					}
  					return {"x":dx, "y":dy}
  				}
    			i++;
  			}
		}
	}

	function renderActionButtons() {
		renderButton("LOAD", 50, 25);
		renderButton("SAVE", 50, 65);
		renderButton("LANGUAGE", 50, 105);
		renderButton("NEW NODE", 50, 145);
		renderButton("DELETE", 50, 185);
		//renderButton("RUN", 50, 225);
		renderButton("START", 50, 265);
		renderButton("KILL", 50, 305);
        
		renderButton("ZOOM OUT", canvas.width - 50, 25);
		renderButton("ZOOM IN", canvas.width - 50, 65);
		renderButton("RESET ZOOM", canvas.width - 50, 105);
		renderButton("RESET VIEW", canvas.width - 50, 145);
        
        if (that.showInfo) {
		  renderButton("< SHOW", canvas.width - 50, canvas.height / 2);
        } else {
		  renderButton("> HIDE", canvas.width - 50, canvas.height / 2);
        }
        
        if (hasParent) {
            renderButton("BACK", 50, 385);
        }
	}

	function renderButton(text, x, y) {
		ctx.beginPath();
		ctx.lineWidth="1";
		ctx.fillStyle = "rgb(244,244,244)";
		ctx.strokeStyle="rgb(128,128,128)";
		ctx.rect(x - 40, y -15, 80, 30);
		ctx.fill();
		ctx.stroke();

		ctx.font = "12px 'Helvetica'";
		ctx.fillStyle = "rgb(128,128,128)";
		ctx.textAlign = 'center';
		ctx.textBaseline = 'center';
		ctx.fillText(text, x, y - 7);

	}

	function printResult() {
		var len = that.result.split("\n").length;
		if (len > 1) {
			ctx.beginPath();
			ctx.lineWidth="1";
			ctx.fillStyle = "rgb(244,244,244)";
			ctx.strokeStyle="rgb(128,128,128)";
			ctx.rect(100, 10, 400, 15 + len * 15);
			ctx.fill();
			ctx.stroke();

			ctx.font = "12px 'Helvetica'";
			ctx.fillStyle = "rgb(128,128,128)";
			ctx.textAlign = 'left';
			ctx.textBaseline = 'top';
			ctx.fillText("Result:", 110, 15);
			var i = 1;
			var split = that.result.split("\n");
			for (var line in split) {
				ctx.fillText(split[line], 110, 15 + i * 15);
				i++;
			}
		}
	}
}