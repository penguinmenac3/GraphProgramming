try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("ADAM Optimizer", "extlib.tensorflow.adamoptimizer", {"step_length": 0.001},
                                   {"graph": "Tensor", "session": "TFSession"},
                                   {"train_step": "Tensor", "session": "TFSession"},
                                   "ADAM Descent Optimizer", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        session = value["session"]
        result = tf.train.AdamOptimizer(self.args["step_length"]).minimize(value["graph"])
        
        if tag:
            return {"train_step": result,"session":session, "tags":{"train_step":tag, "session":tag}}
        else:
            return {"train_step": result, "session":session}
