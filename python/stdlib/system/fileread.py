try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("File (Read as Str)", "stdlib.system.fileread", {"filename": 'test.txt'},
                                   {},
                                   {"result": "String"},
                                   "Read the content of a file as a string.", verbose)
        self.args = args

    def tick(self, value):
        result = ""
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        with open(self.args["filename"], "r") as f:
            result += f.read()
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
