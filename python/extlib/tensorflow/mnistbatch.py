try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Mnist Batch", "extlib.tensorflow.mnistbatch", {},
                                   {"trigger": "Object", "mnist": "MNIST"},
                                   {"batch": "Tensor"},
                                   "Get the next batch from mnist", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "trigger" in value["tags"]:
            tag = value["tags"]["trigger"]
        
        mnist = value["mnist"]
        result = mnist.train.next_batch(50)
        
        if tag:
            return {"batch": result, "tags":{"result":tag}}
        else:
            return {"batch": result}
