try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Cross entropy", "extlib.tensorflow.crossentropy", {"code": 'result = value["val"]'},
                                   {"y_": "Tensor", "y": "Tensor"},
                                   {"y_": "Tensor", "y": "Tensor", "entropy": "Tensor"},
                                   "Calculate the cross entropy", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
            
        y_ = value["y_"]
        y = value["y"]
        
        result = -tf.reduce_sum(y_*tf.log(y))
        
        if tag:
            return {"result": result, "y": y, "y_": y_, "tags":{"result":tag}}
        else:
            return {"result": result, "y": y, "y_": y_}
