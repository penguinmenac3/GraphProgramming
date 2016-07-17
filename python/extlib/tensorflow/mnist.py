try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

from tensorflow.examples.tutorials.mnist import input_data


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("MNIST", "extlib.tensorflow.mnist", {},
                                   {},
                                   {"result": "MNIST"},
                                   "Loads the mnist dataset", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = input_data.read_data_sets("MNIST_data/", one_hot=True)
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
