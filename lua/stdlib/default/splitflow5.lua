local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result["1"] = value.val
    result["2"] = value.val
    result["3"] = value.val
    result["4"] = value.val
    result["5"] = value.val
    return {}
  end
end

function myNode.spec(node)
  node.name = "Splitflow 5"
  node.inputs.val = "Object"
  node.outputs["1"] = "Object"
  node.outputs["2"] = "Object"
  node.outputs["3"] = "Object"
  node.outputs["4"] = "Object"
  node.outputs["5"] = "Object"
  node.desc = "Splits the flow into 5."
end

return myNode
