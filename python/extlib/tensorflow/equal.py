try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Equal", "extlib.tensorflow.equal", {},
                                   {"a": "Tensor", "b": "Tensor"},
                                   {"result": "Tensor"},
                                   "Check for each position if a equals b.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "a" in value["tags"]:
            tag = value["tags"]["a"]
        
        result = tf.equal(value["a"], value["b"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
