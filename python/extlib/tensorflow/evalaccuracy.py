try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Eval Accuracy", "extlib.tensorflow.evalaccuracy", {},
                                   {"trigger": "TFSession", "accuracy": "Tensor", "x": "Tensor", "y_": "Tensor", "x_values": "Tensor", "y_values": "Tensor"},
                                   {"result": "Number"},
                                   "eval the accuracy.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        accuracy = value["accuracy"]
        x = value["x"]
        y_ = value["y_"]
        x_values = value["x_values"]
        y_values = value["y_values"]
        session = value["trigger"]
        result = session.run(accuracy, feed_dict={x: x_values, y_: y_values})
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
