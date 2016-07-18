try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Relu Layer", "extlib.tensorflow.relu", {},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "A ReLU layer in a net.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        graph = value["graph"]
        
        graph = tf.nn.relu(graph)
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
