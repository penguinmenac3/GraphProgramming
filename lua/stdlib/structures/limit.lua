local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result["out"] = value["in"]
    return result
  end
end

function myNode.spec(node)
  node.name = "[TODO] Limit"
  node.inputs["in"] = "Object"
  node.outputs["out"] = "Object"
  node.args["Hz"] = 1.0
  node.desc = "Only pass once per timelimit."
end

return myNode
