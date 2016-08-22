local myNode = {}

function myNode.init(node)
  node.tick = function(value)    
    print(value.val)
    return {}
  end
end

return myNode
