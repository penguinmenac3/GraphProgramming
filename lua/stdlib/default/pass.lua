local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result["out"] = value["in"]
    return result
  end
end

function myNode.spec(node)
  node.name = "Pass"
  node.inputs["in"] = "Object"
  node.outputs["out"] = "Object"
  node.desc = "Pass an object. Does nothing."
end

return myNode
