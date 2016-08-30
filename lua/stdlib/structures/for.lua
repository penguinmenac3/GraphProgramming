local myNode = {}
function myNode.init(node)
  node._iteration = 0
  node.tick = function(value)
    result = {}
    if node._iterations < node.args.n then
      result["loop"] = value["trigger"]
    else
      result["done"] = value["trigger"]
    end
    node._iterations = node._iterations + 1
    return result
  end
end

function myNode.spec(node)
  node.name = "For"
  node.inputs["trigger"] = "Object"
  node.outputs["done"] = "Object"
  node.outputs["loop"] = "Object"
  node.args.n = 1000
  node.desc = "Print a not implemented msg"
end

return myNode
