try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import random

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Train", "extlib.tensorflow.train", {},
                                   {"train_step": "Tensor", "batch": "Tensor", "x": "Tensor", "y_": "Tensor"},
                                   {"result": "Object"},
                                   "Executes a train step", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        train_step = value["train_step"]
        batch = value["batch"]
        x = value["x"]
        y_ = value["y_"]
        train_step.run(feed_dict={x: batch[0], y_: batch[1]})
        result["do_not_kill_me"] = random.random()
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
