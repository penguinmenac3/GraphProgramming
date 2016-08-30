local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = value.val
    return result
  end
end

function myNode.spec(node)
  node.name = "Accept any inputs"
  node.inputs.val = "Object"
  node.outputs.result = "Object"
  node.desc = "Accept any input."
end

return myNode
