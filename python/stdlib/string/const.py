def init(node, global_state):
    def tick(value):
        return {"result": node["args"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "String Const"
    node["outputs"]["result"] = "String"
    node["args"] = "Hello"
    node["desc"] = "Returns the arg on the output."
