try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("MNIST Test", "extlib.tensorflow.mnisttest", {"code": 'result = value["val"]'},
                                   {"mnist": "MNIST"},
                                   {"images": "Tensor", "labels": "Tensor"},
                                   "Get test data from mnist.", verbose, needs_foreground=True)
        self.args = args

    def tick(self, value):
        tag = None
        if "tags" in value and "mnist" in value["tags"]:
            tag = value["tags"]["mnist"]
        
        mnist = value["mnist"]
        images = mnist.test.images
        labels = mnist.test.labels
        
        if tag:
            return {"images": images, "labels": labels, "tags":{"images":tag, "labels":tag}}
        else:
            return {"images": images, "labels": labels,}
