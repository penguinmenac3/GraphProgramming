function CDebugger(url, passwd, renderer) {
    var that = this;
    var ws = new WebSocket("ws://"+url+":9000");
    
    ws.onopen = function() {
        ws.send(passwd);
    }
    
    ws.onmessage = function(data) {
        // TODO do something usefull with the data...
        if(data.data != "") {
            console.log(data);
        }
    };
    
    ws.onclose = function() {
        console.log("Closed connection.");
    }
    
    this.continueBreakpoint = function(node_name) {
        ws.send("continue_"+node_name)
    };
    
    this.close = function() {
        ws.close();
    }
}