try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("HTTP Input", "system.httpinput", {"port":80},
                                   {},
                                   {"get": "Object", "post": "Object", "put": "Object", "delete": "Object"},
                                   "Wait for http requests.", verbose)
        self.args = args

    def tick(self, value):
        tag = None
        getRes = None
        postRes = None
        putRes = None
        deleteRes = None
                
        if tag:
            return {"get": getRes, "post": postRes, "put": putRes, "delete": deleteRes, "tags":{"get": tag, "post": tag, "put": tag, "delete": tag}}
        else:
            return {"get": getRes, "post": postRes, "put": putRes, "delete": deleteRes}
