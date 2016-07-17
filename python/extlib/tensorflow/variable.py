try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Variable", "extlib.tensorflow.variable", {"dimensions": [2,2]},
                                   {"session": "TFSession"},
                                   {"session": "TFSession", "result": "Tensor"},
                                   "A tensorflow variable.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.Variable(tf.zeros(self.args["dimensions"]))
        
        if tag:
            return {"result": result, "session":value["session"], "tags":{"result":tag}}
        else:
            return {"result": result, "session":value["session"]}
