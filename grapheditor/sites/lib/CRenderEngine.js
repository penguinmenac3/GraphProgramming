
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
	this.dotTouchSize = 40;
	this.nodeWidth = 180;
	this.nodeHeight = 60;
	this.tmpLine = null;
	this.result = "";
    this.showInfo = true;
    this.marked = null;
    var clearColor = "white";
    var colorInputNode = "#3CB371";
    var colorAlgorithmNode = "orange";
    var colorStructureNode = "darkslategray";
    var colorDebugNode = "red";
    var colorOutputNode = "indianred";
    var colorConnector = "rgba(128,128,128,0.6)";
    var colorMarked = "rgb(128,128,128)";
    var colorOrigin = "red";
    
    this.setDirty = function() {
        isDirty = 1;
    };
    
    this.setTheme = function(clear, input, algorithm, structural, debug, output, connector, marked, origin) {
        clearColor = clear;
        colorInputNode = input;
        colorAlgorithmNode = algorithm;
        colorStructureNode = structural;
        colorDebugNode = debug;
        colorOutputNode = output;
        colorConnector = connector;
        colorMarked = marked;
        colorOrigin = origin;
        that.setDirty();
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
		ctx.canvas.width = width;
		ctx.canvas.height = height;
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
        if (scale < 0.1) {
            scale = 0.1;
        }
        if (scale > 1.728){
            scale = 1.728;
        }
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
        ctx.fillStyle = clearColor;
		ctx.fillRect(0, 0, width, height);

		/* Render the origin cross */
		ctx.beginPath();
		ctx.lineWidth="1";
		ctx.strokeStyle=colorOrigin;
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

	function renderDot(px, py, marked, fillStyle, name, heat, min_heat, max_heat) {        
        ctx.font = parseInt(that.dotSize/2 * scale) + "px 'Helvetica'";
		ctx.fillStyle = fillStyle;
		ctx.textAlign = 'left';
		ctx.textBaseline = 'top';
        var offsetX = that.dotSize/2 + 4;
        var offsetY = -that.dotSize/4;
		ctx.fillText(name, renderOffsetX * scale + px * scale + width/2 + offsetX * scale, renderOffsetY * scale + py * scale + height/2 + offsetY * scale);
        
		ctx.beginPath();
		ctx.fillStyle = fillStyle;
		if (heat > 0) {
			ctx.fillStyle = rgba(min_heat, max_heat, heat, 0.6);
		}
		ctx.rect(renderOffsetX * scale + px * scale - that.dotSize/2 * scale + width/2,renderOffsetY * scale + py * scale - that.dotSize/2 * scale + height/2,that.dotSize * scale,that.dotSize * scale);
		ctx.fill();
        
        if (!marked) {
		  ctx.lineWidth="0";
		  ctx.strokeStyle=fillStyle;
        } else {
		  ctx.lineWidth="2";
		  ctx.strokeStyle=colorMarked;
		  ctx.stroke();
        }
	}

	function rgba(minimum, maximum, value, alpha) {
		ratio = 2.0 * (value-minimum) / (maximum - minimum);
		b = parseInt(Math.max(0, 255*(1-ratio)));
		r = parseInt(Math.max(0, 255*(ratio-1)));
		g = 255 - b - r
		return "rgba("+r+","+g+","+b+","+alpha+")";
	}

	function renderDotConnection(px1, py1, px2, py2) {
		ctx.beginPath();
		ctx.lineWidth="2";
		ctx.strokeStyle=colorConnector;
		ctx.moveTo(renderOffsetX * scale + px1 * scale + width/2,renderOffsetY * scale + py1 * scale + height/2);
		ctx.lineTo(renderOffsetX * scale + px2 * scale + width/2,renderOffsetY * scale + py2 * scale + height/2);
		ctx.stroke();
	}

	function renderNodeText(text, x, y, offsetX, offsetY, color, size) {
        if (!color) {
            color="rgb(128,128,128)";
        }
		/* Write text with speed and curve info */
		ctx.font = parseInt(size * scale) + "px 'Helvetica'";
		ctx.fillStyle = color;
		ctx.textAlign = 'center';
		ctx.textBaseline = 'top';
		ctx.fillText(text, renderOffsetX * scale + x * scale + width/2 + offsetX * scale, renderOffsetY * scale + y * scale + height/2 + offsetY * scale);
	}

	function renderNodeRect(x, y, marked, fillStyle, running) {
		ctx.beginPath();
		ctx.fillStyle = fillStyle;
		ctx.rect(renderOffsetX * scale + x * scale + width/2-that.nodeWidth/2 * scale,renderOffsetY * scale + y * scale + height/2-that.nodeHeight/2 * scale,that.nodeWidth * scale,that.nodeHeight * scale);
		ctx.fill();
		if (running > 0) {
		  ctx.lineWidth="5";
		  ctx.strokeStyle=rgba(0, 20, running, 1.0);
		  ctx.stroke();
		} else if (!marked) {
		  ctx.lineWidth="0";
		  ctx.strokeStyle=fillStyle;
        } else {
		  ctx.lineWidth="5";
		  ctx.strokeStyle=colorMarked;
		  ctx.stroke();
        }
	}

	function renderNodeDebugArray(node, foregroundColor, fillStyle) {
	    var paneWidth = that.nodeWidth * 2;
	    var paneHeight = that.nodeWidth * 1.5;
	    var x = node.x + that.nodeWidth / 2 + paneWidth / 2;
	    var y = node.y - that.nodeHeight / 2 + paneHeight / 2;
	    var marked = node == that.marked;

		ctx.beginPath();
		ctx.fillStyle = fillStyle;
		ctx.rect(renderOffsetX * scale + x * scale + width/2-paneWidth/2 * scale,renderOffsetY * scale + y * scale + height/2-paneHeight/2 * scale,paneWidth * scale,paneHeight * scale);
		ctx.fill();
        if (!marked) {
		  ctx.lineWidth="0";
		  ctx.strokeStyle=fillStyle;
        } else {
		  ctx.lineWidth="5";
		  ctx.strokeStyle=colorMarked;
		  ctx.stroke();
        }

        var data = node.data;
        var len = data.length;

        var max_x = 0;
        var max_y = 0;
        var xs = 1;
        var ys = 1;
        if (Object.prototype.toString.call( data[0] ) === '[object Array]') {
            if (Object.prototype.toString.call( data[0][0] ) === '[object Array]') {
                polygon = true;
                for (var i = 0; i < len; i++) {
                    for (var j = 0; j < data[i].length; j++) {
                        max_x = Math.max(max_x, Math.abs(data[i][j][0]));
                        max_y = Math.max(max_y, Math.abs(data[i][j][1]));
                        if (data[i][j][0] < 0) {
                            xs = 2;
                        }
                        if (data[i][j][1] < 0) {
                            ys = 2;
                        }
                    }
                }
                for (var i = 0; i < len; i++) {
                    renderLineStrip(data[i], paneWidth, paneHeight, x, y, max_x, max_y, foregroundColor, xs, ys);
                }
            } else {
                points = true;

                for (var i = 0; i < len; i++) {
                    max_x = Math.max(max_x, Math.abs(data[i][0]));
                    max_y = Math.max(max_y, Math.abs(data[i][1]));
                    if (data[i][0] < 0) {
                        xs = 2;
                    }
                    if (data[i][1] < 0) {
                        ys = 2;
                    }
                }
                renderLineStrip(data, paneWidth, paneHeight, x, y, max_x, max_y, foregroundColor, xs, ys);
            }
        } else {
            for (var i = 0; i < len; i++) {
                max_y = Math.max(max_y, Math.abs(data[i]));
                if (data[i] < 0) {
                    ys = 2;
                }
            }
            max_x = len;
            xs = 1;
            for (var i = 0; i < len; i++) {
                data[i] = [i, data[i]];
            }
            renderLineStrip(data, paneWidth, paneHeight, x, y, max_x, max_y, foregroundColor, xs, ys);
        }

        var px1 = - paneWidth / 2 + x + paneWidth * 0.1;
        var px2 = - paneWidth / 2 + x + paneWidth * 0.1 + paneWidth * 0.8;
        var py1 = (2-ys) * paneHeight * 0.4 + y;
        var py2 = (2-ys) * paneHeight * 0.4 + y;
        ctx.beginPath();
		ctx.lineWidth="1";
		ctx.strokeStyle=foregroundColor;
		ctx.moveTo(renderOffsetX * scale + px1 * scale + width/2,renderOffsetY * scale + py1 * scale + height/2);
		ctx.lineTo(renderOffsetX * scale + px2 * scale + width/2,renderOffsetY * scale + py2 * scale + height/2);
		ctx.stroke();

		var px1 = -(2-xs) * paneWidth * 0.4 + x;
        var px2 = -(2-xs) * paneWidth * 0.4 + x;
        var py1 = - paneHeight / 2 + y + paneHeight * 0.1;
        var py2 = - paneHeight / 2 + y + paneHeight * 0.1 + paneHeight * 0.8;
        ctx.beginPath();
		ctx.lineWidth="1";
		ctx.strokeStyle=foregroundColor;
		ctx.moveTo(renderOffsetX * scale + px1 * scale + width/2,renderOffsetY * scale + py1 * scale + height/2);
		ctx.lineTo(renderOffsetX * scale + px2 * scale + width/2,renderOffsetY * scale + py2 * scale + height/2);
		ctx.stroke();

        renderNodeText("Y: " + Math.floor(max_y*1000)/1000.0, x-paneWidth*0.5+30, y-paneHeight*0.5+4, 0, 0, foregroundColor, 16);
        renderNodeText("X: " + Math.floor(max_x*1000)/1000.0, x+paneWidth*0.5-30, y+paneHeight*0.5-20, 0, 0, foregroundColor, 16);
	}

	function renderLineStrip(data, paneWidth, paneHeight, x, y, max_x, max_y, foregroundColor, xs, ys) {
        var len = data.length;
	    for (var i = 1; i < len; i++) {
            var px1 = ((xs-1)/2 + data[i-1][0]/(xs*max_x)) * paneWidth * 0.8  - paneWidth / 2  + x + paneWidth * 0.1;
            var px2 = ((xs-1)/2 + data[i][0]  /(xs*max_x)) * paneWidth * 0.8  - paneWidth / 2  + x + paneWidth * 0.1;
            var py1 = (1/ys - data[i-1][1]/(ys*max_y)) * paneHeight * 0.8 - paneHeight / 2 + y + paneHeight * 0.1;
            var py2 = (1/ys - data[i][1]  /(ys*max_y)) * paneHeight * 0.8 - paneHeight / 2 + y + paneHeight * 0.1;
            ctx.beginPath();
		    ctx.lineWidth="2";
		    ctx.strokeStyle=foregroundColor;
		    ctx.moveTo(renderOffsetX * scale + px1 * scale + width/2,renderOffsetY * scale + py1 * scale + height/2);
		    ctx.lineTo(renderOffsetX * scale + px2 * scale + width/2,renderOffsetY * scale + py2 * scale + height/2);
		    ctx.stroke();
        }
	}

	function renderNodeDebugImage(node, foregroundColor, fillStyle) {
	    var paneWidth = that.nodeWidth * 2;
	    var paneHeight = that.nodeWidth * 1.5;
	    var x = node.x + that.nodeWidth / 2 + paneWidth / 2;
	    var y = node.y - that.nodeHeight / 2 + paneHeight / 2;
	    var marked = node == that.marked;

		ctx.beginPath();
		ctx.fillStyle = fillStyle;
		ctx.rect(renderOffsetX * scale + x * scale + width/2-paneWidth/2 * scale,renderOffsetY * scale + y * scale + height/2-paneHeight/2 * scale,paneWidth * scale,paneHeight * scale);
		ctx.fill();
        if (!marked) {
		  ctx.lineWidth="0";
		  ctx.strokeStyle=fillStyle;
        } else {
		  ctx.lineWidth="5";
		  ctx.strokeStyle=colorMarked;
		  ctx.stroke();
        }

        var img = node.data_img;
        ctx.drawImage(img,renderOffsetX * scale + x * scale + width/2-paneWidth/2 * scale,renderOffsetY * scale + y * scale + height/2-paneHeight/2 * scale,paneWidth * scale,paneHeight * scale)
	}

	function renderGraph() {
		if (WebUI.graph != null) {
			graph = WebUI.graph;
			graph.connections.forEach(function(connection) {
				renderConnection(graph, connection);
			});
			min_heat = Number.MAX_VALUE;
			max_heat = 0;
			graph.nodes.forEach(function(node) {
				if (typeof node.heat === "undefined") {
					node.heat = 0;
				}
				if (typeof node.running === "undefined") {
					node.running = 0;
				}
				min_heat = Math.min(min_heat, node.heat);
				max_heat = Math.max(max_heat, node.heat);
			});
			//console.log(min_heat);
			//console.log(max_heat);
			graph.nodes.forEach(function(node) {
				renderNode(node, min_heat, max_heat);
			});
		}
	}

	that.cooldown = function() {
		if (WebUI.graph != null) {
			graph = WebUI.graph;
			
			graph.nodes.forEach(function(node) {
				if (typeof node.running === "undefined") {
					node.running = 0;
				}
				if (node.running < 20) {
					node.running -= 1;
				}
				node.running = Math.max(0, node.running);
			});
		}
	}

	that.resetHeat = function() {
		if (WebUI.graph != null) {
			graph = WebUI.graph;
			
			graph.nodes.forEach(function(node) {
				node.running = 0;
				node.heat = 0;
			});
		}
	}

	function renderConnection(graph, connection) {
		pos1 = that.getNodeOutputPosition(graph, connection.input.node, connection.input.output);
		pos2 = that.getNodeInputPosition(graph, connection.output.node, connection.output.input);
		renderDotConnection(pos1.x, pos1.y, pos2.x, pos2.y);
	}

	function renderNode(node, min_heat, max_heat) {
		if (typeof node.x === "undefined" || typeof node.y === "undefined") {
			node.x = -renderOffsetX;
			node.y = -renderOffsetY;
			console.log("Default position for: " + node.name)
		}
        
        var fillStyle = colorConnector;
        var foregroundColor = "white";
        var fillStyleLarge = colorAlgorithmNode;
		var nodePackage = node.code.split(".")[1];
        if (Object.keys(node.inputs).length == 0) {
            fillStyleLarge = colorInputNode;
        } else if (Object.keys(node.outputs).length == 0) {
            fillStyleLarge = colorOutputNode;
        } else if (nodePackage.lastIndexOf("structures", 0) === 0 || (nodePackage.lastIndexOf("default", 0) === 0 && nodePackage.lastIndexOf("function", "default.".length) < 0)) {
            fillStyleLarge = colorStructureNode;
        } else if (nodePackage.lastIndexOf("debug") === 0) {
            fillStyleLarge = colorDebugNode;
        }

		/* Draw rect symbol for robot */
		renderNodeRect(node.x, node.y, node == that.marked, fillStyleLarge, node.running);
		if (node.data && node.data != null) {
		    if( Object.prototype.toString.call( node.data ) === '[object Array]' ) {
		        renderNodeDebugArray(node, foregroundColor, colorConnector);
		    }
		    else if( node.data  == 'image' ) {
		        var image = null;
                    if (node.data_img && node.data_img != null && Object.prototype.toString.call( node.data_img ) === '[object HTMLImageElement]') {
                        image = node.data_img;
                    } else {
                        image = new Image()
                    }
                    image.src = 'data:image/png;base64,' + node.data_str;
                    node.data_img = image;
		        renderNodeDebugImage(node, foregroundColor, colorConnector);
		    } else {
		        console.log(Object.prototype.toString.call( node.data ));
		    }
		}

		/* Write text with speed and curve info */
        var nname = node.displayname;
		if (typeof node.desc === "undefined") {
			node.desc = {};
		}
        if (node.desc != {} && node.desc != "" && node.desc != null) {
		  renderNodeText(nname, node.x, node.y, 0, -15, foregroundColor, 16);
		  renderNodeText(node.desc, node.x, node.y, 0,  10, foregroundColor, 12);
        } else {
		  renderNodeText(nname, node.x, node.y, 0, -6, foregroundColor, 16);
        }
		//renderNodeText(node.desc, node.x, node.y, 0,  15, foregroundColor);

		for (var key in node.inputs) {
  			if (node.inputs.hasOwnProperty(key)) {
  				pos = getPosition(node, key, node.inputs, true);
    			renderDot(pos.x, pos.y, node == that.marked, fillStyle, key, node.heat, min_heat, max_heat);
  			}
		}
		for (var key in node.outputs) {
  			if (node.outputs.hasOwnProperty(key)) {
  				pos = getPosition(node, key, node.outputs, false);
				isRunningDelta = 0;
				if (node.running == 20) {
					isRunningDelta = 1;
				}
    			renderDot(pos.x, pos.y, node == that.marked, fillStyle, key, node.heat - isRunningDelta, min_heat, max_heat);
  			}
		}
		//renderDot(node.x - that.nodeWidth/2 + that.dotSize / 2, node.y - that.nodeHeight/2 + that.dotSize / 2, node == that.marked, fillStyle);
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
		renderButton("LOAD", 50, 25, colorStructureNode);
		renderButton("SAVE", 50, 65, colorStructureNode);
		renderButton("LANGUAGE", 50, 105, colorStructureNode);
		renderButton("NEW NODE", 50, 145, colorAlgorithmNode);
		renderButton("DELETE", 50, 185, colorOutputNode);
		//renderButton("RUN", 50, 225, "dimgray");
		//renderButton("START", 50, 265, colorInputNode);
		//renderButton("KILL", 50, 305, colorOutputNode);
        
		renderButton("ZOOM OUT", canvas.width - 50, 25, colorStructureNode);
		renderButton("ZOOM IN", canvas.width - 50, 65, colorStructureNode);
		renderButton("RESET ZOOM", canvas.width - 50, 105, colorOutputNode);
		renderButton("RESET VIEW", canvas.width - 50, 145, colorOutputNode);
        
        if (that.showInfo) {
		  renderButton("< SHOW", canvas.width - 50, canvas.height / 2, colorInputNode);
        } else {
		  renderButton("> HIDE", canvas.width - 50, canvas.height / 2, colorOutputNode);
        }
        
        if (hasParent) {
            renderButton("BACK", 50, 385, "dimgray");
        }
	}

	function renderButton(text, x, y, color) {
		ctx.beginPath();
		ctx.fillStyle = color;
		ctx.rect(x - 40, y -15, 80, 30);
		ctx.fill();

		ctx.font = "12px 'Helvetica'";
		ctx.fillStyle = "white";
		ctx.textAlign = 'center';
		ctx.textBaseline = 'top';
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