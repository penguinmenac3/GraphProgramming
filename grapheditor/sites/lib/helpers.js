
function attachEvent(obj, event, callback) {
	/*
	 * Fallunterscheidung automatisch, damit man es nicht immer manuell machen
	 * muss
	 */
	if (obj.addEventListener)
		obj.addEventListener(event, callback, false);
	else if (obj.attachEvent)
		obj.attachEvent('on' + event, callback);
	else
		obj['on' + event] = callback;
}

function getGraph(graph, callback, callbackFailure) {
    var params = "getgraph=" + graph;
    sendViaPost(params, callback, callbackFailure)
}

function getNodes(graph, callback, callbackFailure) {
    var params = "getnodes=" + graph;
    sendViaPost(params, callback, callbackFailure)
}

function setGraph(graph, data, callback, callbackFailure) {
    var params = "setgraph=" + graph + "&value=" + escape(JSON.stringify(data));
    sendViaPost(params, callback, callbackFailure)
}

function sendViaPost(params, callback, callbackFailure) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText != "") {
                if (callback != null) {
                    var inobject = JSON.parse(xmlhttp.responseText);
                    callback(inobject);
                }
            }
        } else if (xmlhttp.readyState==4) {
            if (callbackFailure != null) {
                callbackFailure(xmlhttp.responseText);
            }
        }
    }
    xmlhttp.open("POST", "/api",true);
    //Send the proper header information along with the request
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(params);
}

function execute(graph, callback, callbackFailure) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText != "") {
                if (callback != null) {
                    callback(xmlhttp.responseText);
                }
            }
        } else if (xmlhttp.readyState==4) {
            if (callbackFailure != null) {
                callbackFailure(xmlhttp.responseText);
            }
        }
    }
    var params = "execGraph=" + graph;
    xmlhttp.open("POST", "/api",true);
    //Send the proper header information along with the request
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(params);
}

function sendViaGet(params, callback, callbackFailure) {
	var xmlhttp;
    if (window.XMLHttpRequest) {
    	xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
    	if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText != "") {
                if (callback != null) {
                    var inobject = JSON.parse(xmlhttp.responseText);
                    callback(inobject);
                }
            }
        } else if (xmlhttp.readyState==4) {
            if (callbackFailure != null) {
                callbackFailure(xmlhttp.responseText);
            }
        }
    }
    xmlhttp.open("POST", "/api?"+params,true);
    xmlhttp.send();
}