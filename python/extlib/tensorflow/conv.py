try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Conv Layer", "extlib.tensorflow.conv", {"stddev": 0.1, "patch_x": 5, "patch_y": 5, "input_channels": 1, "output_channels": 32},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "A convolution layer in a net.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        graph = value["graph"]
        
        stddev = self.args["stddev"]
        patch_x = self.args["patch_x"]
        patch_y = self.args["patch_y"]
        input_channels = self.args["input_channels"]
        output_channels = self.args["output_channels"]
                
        W_shape = [patch_x, patch_y, input_channels, output_channels]
        b_shape = [output_channels]
        
        initial_w = tf.truncated_normal(W_shape, stddev=stddev)
        initial_b = tf.constant(stddev, shape=b_shape)
        
        W = tf.Variable(initial_w)
        b = tf.Variable(initial_b)
        
        graph = tf.nn.conv2d(graph, W, strides=[1, 1, 1, 1], padding='SAME') + b
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
