try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Session", "extlib.tensorflow.session", {},
                                   {},
                                   {"result": "TFSession"},
                                   "A tensorflow session.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.Session() 
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
