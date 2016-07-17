try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Argmax", "extlib.tensorflow.argmax", {"param": 1},
                                   {"val": "Tensor"},
                                   {"result": "Tensor"},
                                   "tf.argmax(val, param)", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.argmax(value["val"], self.args["param"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
