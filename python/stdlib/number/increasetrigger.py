import time

try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Increase Trigger Number", "stdlib.number.increasetrigger", {"start":0,"stop": 100, "time":1.0},
                                   {}, {"result": "Number"}, "Trigger value every time seconds.", verbose, True, True)
        self.args = args
        self.index = None

    def tick(self, value):
        if self.index is None:
            self.index = self.args["start"]
        time.sleep(self.args["time"])
        
        result = self.index
        
        if self.index > self.args["stop"]:
            result = None
        
        self.index += 1
        return {"result": result}
