try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import json
import sys
try:
    import base64
    import numpy as np
    import cv2
except:
    pass # well there cannot be any cv input, no error will occur.

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("View", "stdlib.debug.view", {},
                                   {"val": "Object"},
                                   {"result": "Object"},
                                   "Views (in IDE) and passes the object.", verbose)
        self.args = args

    def tick(self, value):
        result = {}
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]

        if "debugger" in builtins.registry:
            data_str = ""
            if type(value["val"]) is list or type(value["val"]) is dict or type(value["val"]) is str or type(value["val"]) is int:
                data_str = "json:" + json.dumps(value["val"])
            elif type(value["val"]) == np.ndarray:
                img = value["val"]
                img = cv2.resize(img.copy(), (160, 120), 0, 0, cv2.INTER_CUBIC)
                cnt = cv2.imencode('.png', img)[1]
                b64 = base64.encodestring(cnt)
                data_str = ("img:" + b64).replace("\n", "")
            else:
                data_str = "type:" + str(type(value["val"]))
            builtins.registry["debugger"].send("data_"+self.node_uid+":"+data_str)

        result = value["val"]

        if tag:
            return {"result": result, "tags":{"result":tag}}
        else:
            return {"result": result}
