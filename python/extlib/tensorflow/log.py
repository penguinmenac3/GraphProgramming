try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Log", "extlib.tensorflow.log", {},
                                   {"val": "Tensor"},
                                   {"result": "Tensor"},
                                   "Calculate log(val)", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.log(value["val"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
