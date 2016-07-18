try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Reshape 2 FC Layer", "extlib.tensorflow.reshape2fc", {"img_width": 7, "img_height": 7, "input_channels": 64},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   {"session": "TFSession", "graph": "Tensor"},
                                   "Reshape for fully connected.", verbose, needs_foreground=True)
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
        input_channels = self.args["input_channels"]
        
        graph = tf.reshape(graph, [-1,img_width * img_height * input_channels])
        
        if tag:
            return {"session": session, "graph": graph, "tags":{"result":tag}}
        else:
            return {"session": session, "graph": graph}
