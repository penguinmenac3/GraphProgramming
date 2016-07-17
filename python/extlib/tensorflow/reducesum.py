try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Reduce Sum", "extlib.tensorflow.reducesum", {"code": 'result = value["val"]'},
                                   {"val": "Tensor"},
                                   {"result": "Tensor"},
                                   "Reduce the sum", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.reduce_sum(value["val"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
