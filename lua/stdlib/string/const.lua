local myNode = {}

function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = node.args
    return result
  end
end

return myNode
