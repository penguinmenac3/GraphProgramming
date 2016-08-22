local myNode = {}

function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.result = node.args
    return result
  end
end

function myNode.spec(node)
  node.name = "String Const"
  node.outputs.result = "String"
  node.args = "Hello"
  node.desc = "Returns the arg on the output."
end

return myNode
