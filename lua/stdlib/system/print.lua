local myNode = {}

function myNode.init(node)
  node.tick = function(value)    
    print(value.val)
    return {}
  end
end

function myNode.spec(node)
  node.name = "Print"
  node.inputs.val = "Object"
  node.desc = "Print on the screen."
end

return myNode
