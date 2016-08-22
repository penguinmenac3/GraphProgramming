local myNode = {}

function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = value.left .. value.right
    return result
  end
end

function myNode.spec(nod)
  node.name = "String Concat"
  node.inputs.left = "String"
  node.inputs.right = "String"
  node.outputs.result = "Object"
  node.desc = "Concat left and right."
end

return myNode
