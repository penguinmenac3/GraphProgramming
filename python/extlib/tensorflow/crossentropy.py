try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Cross entropy", "extlib.tensorflow.crossentropy", {"code": 'result = value["val"]'},
                                   {"y_": "Tensor", "y": "Tensor"},
                                   {"result": "Tensor"},
                                   "Calculate the cross entropy", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = -tf.reduce_sum(value["y_"]*tf.log(value["y"]))
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
