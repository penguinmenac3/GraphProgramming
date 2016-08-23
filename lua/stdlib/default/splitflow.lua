local myNode = {}

function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.left = value.val
    result.right = value.val
    return result
  end
end

function myNode.spec(node)
  node.name = "Splitflow 2"
  node.inputs.val = "Object"
  node.outputs.left = "Object"
  node.outputs.right = "Object"
  node.desc = "Split the flow into two."
end

return myNode
