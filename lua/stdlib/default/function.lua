local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = value.val
    print("Not implemented yet: " .. node.code)
    return result
  end
end

function myNode.spec(node)
  node.name = "Function"
  node.inputs.val = "Object"
  node.outputs.result = "Object"
  node.args.code = "result.result = value.val"
  node.desc = "Execute a custom function"
end

return myNode
