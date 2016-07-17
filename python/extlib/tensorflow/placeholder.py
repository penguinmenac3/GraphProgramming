try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Placeholder", "extlib.tensorflow.placeholder", {"batch_size":None, "dimension": 0},
                                   {},
                                   {"result": "Object"},
                                   "A tensorflow placeholder.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.placeholder(tf.float32, shape=[self.args["batch_size"], self.args["dimension"]])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
