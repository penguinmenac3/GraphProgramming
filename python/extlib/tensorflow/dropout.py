try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Dropout Layer", "extlib.tensorflow.dropout", {},
                                   {"session": "TFSession", "graph": "Tensor", "keep_prob": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "A linear layer in a net.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        graph = value["graph"]
        keep_prob = value["keep_prob"]
        
        graph = tf.nn.dropout(graph, keep_prob)
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
