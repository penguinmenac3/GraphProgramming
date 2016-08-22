local myNode = {}

function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = value.left .. value.right
    return result
  end
end

return myNode
