try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Mnist Batch", "extlib.tensorflow.mnistbatch", {},
                                   {"val": "Object", "mnist": "MNIST"},
                                   {"result": "Tensor"},
                                   "Get the next batch from mnist", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        result = mnist.train.next_batch(50)
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
