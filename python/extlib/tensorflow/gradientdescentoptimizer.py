try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import tensorflow as tf


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("GD Optimizer", "extlib.tensorflow.gradientdescentoptimizer", {"step_length": 0.01},
                                   {"val": "Tensor"},
                                   {"train_step": "Tensor"},
                                   "Gradient Descent Optimizer", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = tf.train.GradientDescentOptimizer(self.args["step_length"]).minimize(value["val"])
        
        if tag:
            return {"train_step": result, "tags":{"train_step":tag}}
        else:
            return {"train_step": result}
