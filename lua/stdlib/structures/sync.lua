local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.a = value.a
    result.b = value.b
    return result
  end
end

function myNode.spec(node)
  node.name = "Sync"
  node.inputs.a = "Object"
  node.inputs.b = "Object"
  node.outputs.a = "Object"
  node.outputs.b = "Object"
  node.desc = "Only pass if both are there."
end

return myNode
