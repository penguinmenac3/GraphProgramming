try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Query Database", "extlib.database.query", {"code": 'c = db.cursor()\nresult = value["val"]', "db_id": "bla"},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Interact with a db.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        db = builtins.registry["db"][self.args["db_id"]]
        
        exec(self.args["code"])
        
        if builtins.registry["db_types"][self.args["db_id"]] == "sqlite":
          db.commit()
        
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
