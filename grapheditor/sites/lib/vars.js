/* Keymapping */
var KEY_F1 = 112;
var KEY_F2 = 113;
var KEY_F3 = 114;
var KEY_F4 = 115;
var KEY_F5 = 116;
var KEY_F6 = 117;
var KEY_F7 = 118;
var KEY_F8 = 119;
var KEY_F9 = 120;
var KEY_F10 = 121;
var KEY_F11 = 122;
var KEY_F12 = 123;

var KEY_0 = 48;
var KEY_1 = 49;
var KEY_2 = 50;
var KEY_3 = 51;
var KEY_4 = 52;
var KEY_5 = 53;
var KEY_6 = 54;
var KEY_7 = 55;
var KEY_8 = 56;
var KEY_9 = 57;

var KEY_A = 65;
var KEY_B = 66;
var KEY_C = 67;
var KEY_D = 68;
var KEY_E = 69;
var KEY_F = 70;
var KEY_G = 71;
var KEY_H = 72;
var KEY_I = 73;
var KEY_J = 74;
var KEY_K = 75;
var KEY_L = 76;
var KEY_M = 77;
var KEY_N = 78;
var KEY_O = 89;
var KEY_P = 80;
var KEY_Q = 81;
var KEY_R = 82;
var KEY_S = 83;
var KEY_T = 84;
var KEY_U = 85;
var KEY_V = 86;
var KEY_W = 87;
var KEY_X = 88;
var KEY_Y = 89;
var KEY_Z = 90;

var KEY_LEFT = 37;
var KEY_RIGHT = 39;
var KEY_UP = 38;
var KEY_DOWN = 40;
var KEY_PAGE_UP = 33;
var KEY_PAGE_DOWN = 34;
var KEY_SPACE = 32;
var KEY_ENTER = 13;
var KEY_BACKSPACE = 8;
var KEY_ESCAPE = 27;
var KEY_SHIFT = 16;
var KEY_CTRL = 17;
var KEY_ALT = 18;
var KEY_TAB = 9;
var KEY_CAPSLOCK = 20;
var KEY_TILDE = 192;
var KEY_PAUSE = 19;
var KEY_PLUS = 187;
var KEY_MINUS = 189;
var KEY_NEG_ROTATION = 222;
var KEY_POS_ROTATION = 191;

var BUTTON_LEFT = 1;
var BUTTON_MIDDLE = 2;
var BUTTON_RIGHT = 3;

/* internal stuff, very important (atm) */
var data_width = 1024;
var data_height = 768;

/* extending the window API */
window.requestNextAnimationFrame = (function () {
	return window.requestAnimationFrame || window.webkitRequestAnimationFrame
	|| window.mozRequestAnimationFrame  || window.oRequestAnimationFrame
	 || window.msRequestAnimationFrame ||
	function (callback, element) {
		var self = this, start, finish;
		window.setTimeout( function() {
			start = +new Date();
			callback(start);
			finish = +new Date();
			self.timeout = 1000 / 60 - (finish - start);
		}, self.timeout);
	};
})();
