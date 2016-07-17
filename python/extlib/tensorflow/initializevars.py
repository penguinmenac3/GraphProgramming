try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Initialize Variables", "extlib.tensorflow.initializevars", {"code": 'result = value["val"]'},
                                   {"session": "TFSession"},
                                   {"session": "TFSession"},
                                   "Initialize vars in session.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "session" in value["tags"]:
            tag = value["tags"]["session"]
        
        result = value["session"]
        value["session"].run(tf.initialize_all_variables())
        
        if tag:
            return {"session": result, "tags":{"session":tag}}
        else:
            return {"session": result}
