local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = node.args
    return result
  end
end

function myNode.spec(node)
  node.name = "Const"
  node.outputs.result = "Boolean"
  node.args = true
  node.desc = "Return a const boolean"
end

return myNode
