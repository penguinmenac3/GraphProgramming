try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Reshape 2 Conv Layer", "extlib.tensorflow.reshape2conv", {"img_width": 28, "img_height": 28, "output_channels": 1},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "Reshape for convolution.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        graph = value["graph"]
        
        img_width = self.args["img_width"]
        img_height = self.args["img_height"]
        output_channels = self.args["output_channels"]
        
        graph = tf.reshape(graph, [-1,img_width,img_height,output_channels])
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
