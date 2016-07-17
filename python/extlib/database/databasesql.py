try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import MySQLdb as mdb
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Database SQL", "extlib.database.databasesql", {"db_id": "bla", "db": "bla", "user": "bla", "password": "bla", "host": "localhost"},
                                   {},
                                   {},
                                   "Creates a connection to a database.", verbose, True, False)
        self.args = args

    def tick(self, value):
        if not "db" in builtins.registry:
            builtins.registry["db"] = {}
            builtins.registry["db_types"] = {}
        db = mdb.connect(self.args["host"], self.args["user"], self.args["password"], self.args["db"])
        builtins.registry["db"][self.args["db_id"]] = db
        builtins.registry["db_types"][self.args["db_id"]] = "sql"
        builtins.shutdown_hook.append(db.close)
        return {}
