try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("File (Write as str)", "stdlib.system.filewrite", {"filename": "../test.txt"},
                                   {"val": "String"},
                                   {},
                                   "Write string to file (OVERWRITE).", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        with open(self.args["filename"], "w") as f:
            f.truncate()
            f.write(value["val"])
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
