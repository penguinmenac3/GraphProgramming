function CDebugger(url, passwd, ui, renderer) {
    var that = this;
    var ws = new WebSocket("ws://"+url+":9000");
    
    ws.onopen = function() {
        ws.send(passwd);
    }
    
    ws.onmessage = function(data) {
        if(data.data != "") {
            var d = data.data.split(":");
            var node = d[0].split("_")[1];
            var data_type = d[1];
            var data_data = "";
            for (var i = 2; i < d.length; i++) {
                if (i > 2) {
                    data_data += ":" + d[i];
                } else {
                    data_data += d[i];
                }
            }
            if (data_type == "running") {
                var node_obj = ui.findNode(node);
                if (node_obj == null) {
                    console.log("Cannot find node: " + node);
                } else {
                    console.log(data_data);
                    renderer.cooldown();
                    var data_obj = JSON.parse(data_data);
                    node_obj.heat = data_obj["heat"];
                    if (data_obj["state"]) {
                        node_obj.running = 20;
                    } else {
                        node_obj.running = 19;
                    }
                    renderer.cooldown();
                    renderer.setDirty();
                }
            } else if (data_type == "json") {
                var node_obj = ui.findNode(node);
                if (node_obj == null) {
                    console.log("Cannot find node: " + node);
                } else {
                    var data_obj = JSON.parse(data_data);
                    node_obj.data = data_obj;
                    renderer.setDirty();
                }
            } else if (data_type == "img") {
                var node_obj = ui.findNode(node);
                if (node_obj == null) {
                    console.log("Cannot find node: " + node);
                } else {
                    node_obj.data = "image";
                    node_obj.data_str = data_data;
                    renderer.setDirty();
                }
            } else {
                console.log(data.data);
                console.log(data_type);
                console.log(data_data);
            }
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