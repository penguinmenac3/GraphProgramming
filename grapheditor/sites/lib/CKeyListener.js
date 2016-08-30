
function WebUI_CKeyListener() {
	var that = this;
	var RenderEngine = null;
	var running = false;
    var lastPos = {x: 0, y: 0};
	/* fps mesurement */
	var fps = 60;
	var fps_timestamp = new Date().getTime();

	/* mousemovement */
	var mouse = {
		isDown : false,
		pos : null
	};

	/* registers mousedown event */
	function onmousedown(e) {
		if (e.which == BUTTON_LEFT) {
			mouse.pos = getCursorPosition(e);
			mouse.isDown = true;
            var scale = RenderEngine.getScale();
			var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
			var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
			WebUI.trySelect(dx, dy);
		}
	}

	/* if mouse is not dragged call mouse-click-listener */
	function onmouseup(e) {
		if (e.which == BUTTON_LEFT) {
			mouse.isDown = false;
			mouse.pos = getCursorPosition(e);
            var scale = RenderEngine.getScale();
			var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
			var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
			WebUI.unselect(dx, dy);
		}
	}
	/* Here the free movement is implemented (on mouse drag) */
	function onmousemove(e) {
		if (mouse.isDown == true) {
			mouse.pos = getCursorPosition(e);
            var scale = RenderEngine.getScale();
			var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
			var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
			WebUI.moveSelected(dx, dy);
		}
	}

	/* registers mousedown event */
	function ontouchstart(e) {
		mouse.pos = getCursorPosition(e);
		mouse.isDown = true;
        var scale = RenderEngine.getScale();
		var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
		var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
		WebUI.trySelect(dx, dy);
		e.preventDefault();
	}

	/* if mouse is not dragged call mouse-click-listener */
	function ontouchend(e) {
		mouse.isDown = false;
		mouse.pos = getCursorPosition(e);
        var scale = RenderEngine.getScale();
		var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
		var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
		WebUI.unselect(dx, dy);
		e.preventDefault();
	}
	/* Here the free movement is implemented (on mouse drag) */
	function ontouchmove(e) {
		mouse.pos = getCursorPosition(e);
        var scale = RenderEngine.getScale();
		var dx = mouse.pos.x - RenderEngine.getSize().width / 2 - RenderEngine.getOffsetX() * scale; 
		var dy = mouse.pos.y - RenderEngine.getSize().height / 2 - RenderEngine.getOffsetY() * scale;
		WebUI.moveSelected(dx, dy);
		e.preventDefault();
	}

	function onkeydown(e) {
		var key = e.keyCode;
	}

	function toggle_fullscreen() {
		RenderEngine.toggleFullscreen();
	}
	/* force a certain fullscreen state */
	function force_fullscreen(b_full) {
		RenderEngine.forceFullscreen();
	}
	
	/* update cursor position (required for free mode) */
	function getCursorPosition(e) {
		var pos = {
			x: 0, y: 0}
		;
		if (e.pageX != undefined && e.pageY != undefined) {
			pos.x = e.pageX;
			pos.y = e.pageY;
		}
		else {
			pos.x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
			pos.y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
		}
        
        if (typeof(pos.x) === "undefined" || typeof(pos.y) === "undefined" || pos.x == 0 || pos.y == 0 || isNaN(pos.x) || isNaN(pos.y)) {
            for (var i = 0; i < e.touches.length; i++) {
			    pos.x = e.touches[0].pageX;
			    pos.y = e.touches[0].pageY;
  		    }
  		}
        //console.log(pos);
        if (pos.x == 0 || pos.y == 0 || isNaN(pos.x) || isNaN(pos.y)) {
            pos.x = lastPos.x;
            pos.y = lastPos.y;
        } else {
            lastPos.x = pos.x;
            lastPos.y = pos.y;
        }
		var canv_pos = RenderEngine.getCanvasPosition();
		pos.x -= canv_pos.x;
		pos.y -= canv_pos.y;
		return pos;
	}

	/* keep the framerate high and calculate it for correct displaying */
	function nextFrame() {
		fps = 1000.0 / (new Date().getTime() - fps_timestamp);
		fps_timestamp = new Date().getTime();
		if (WebUI.debug == true) {
			window.setTimeout(move, 0);
			//window.requestNextAnimationFrame(move);
		} else {
			window.requestNextAnimationFrame(move);
		}
	}

	/* the heartbeat */
	function move() {
		RenderEngine.render(fps);
		/* break the infinite loop */
		if (running == true)
			nextFrame();
	}

	this.launch = function(Param_RenderEngine) {
		RenderEngine = Param_RenderEngine;
		running = true;
		nextFrame();
	};

	this.init = function(canvas) {
		attachEvent(canvas, 'mousedown', onmousedown);
		attachEvent(canvas, 'mouseup', onmouseup);
		attachEvent(canvas, 'mousemove', onmousemove);
		attachEvent(canvas, 'touchstart', ontouchstart);
		attachEvent(canvas, 'touchmove', ontouchmove);
		attachEvent(canvas, 'touchend', ontouchend);
		window.onkeydown = onkeydown;
	};

	this.stop = function() {
		running = false;
	};
}
