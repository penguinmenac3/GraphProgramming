try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import sqlite3
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Database SQLite", "extlib.database.databasesqlite", {"db_id": "bla", "file": "bla.db"},
                                   {},
                                   {},
                                   "Setup the database as SQLite.", verbose, True, False)
        self.args = args

    def tick(self, value):
        if not "db" in builtins.registry:
            builtins.registry["db"] = {}
            builtins.registry["db_types"] = {}
        db = sqlite3.connect(self.args["file"])
        builtins.registry["db"][self.args["db_id"]] = db
        builtins.registry["db_types"][self.args["db_id"]] = "sqlite"
        builtins.shutdown_hook.append(db.close)
        return {}
