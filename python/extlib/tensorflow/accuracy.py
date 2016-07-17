try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Accuracy", "extlib.tensorflow.accuracy", {},
                                   {"y": "Tensor", "y_": "Tensor"},
                                   {"result": "Tensor"},
                                   "Accuracy model.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        y = value["y"]
        y_ = value["y_"]
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        result = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
