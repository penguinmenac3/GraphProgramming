try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Complete Linear Layer", "extlib.tensorflow.linearcomplete", {"in_dimension": 100, "out_dimension": 10, "stddev": 0.1},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "A linear + ReLU layer in a net.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        graph = value["graph"]
        
        W_shape = [self.args["in_dimension"], self.args["out_dimension"]]
        b_shape = [self.args["out_dimension"]]
        stddev = self.args["stddev"]
        
        initial_w = tf.truncated_normal(W_shape, stddev=stddev)
        initial_b = tf.constant(stddev, shape=b_shape)
        W = tf.Variable(initial_w)
        b = tf.Variable(initial_b)
        
        graph = tf.nn.relu(tf.matmul(graph, W) + b)
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
