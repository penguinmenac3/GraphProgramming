local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result["true"] = nil
    result["false"] = nil
    if value.condition then
      result["true"] = value.val
    else
      result["false"] = value.val
    end
    return result
  end
end

function myNode.spec(node)
  node.name = "If"
  node.inputs.val = "Object"
  node.inputs.condition = "Boolean"
  node.outputs["true"] = "Object"
  node.outputs["false"] = "Object"
  node.desc = "Pass val based on condition."
end

return myNode
