try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Multiply (:Componentwise)", "stdlib.arrays.multcomp", {},
                                   {"a": "Array", "b": "Array"},
                                   {"result": "Array"},
                                   "Multiply two arrays componentwise.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        a = value["a"]
        b = value["b"]
        result = []
        al = len(a)
        bl = len(b)
        if not al == bl:
          print("ERROR: Size missmatch")
          return {"result": None}
        
        for x in range(al):
            result.append(0)
            result[x] += a[x] * b[x]
                    
        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
