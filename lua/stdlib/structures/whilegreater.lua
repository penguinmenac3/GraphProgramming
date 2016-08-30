local myNode = {}
function myNode.init(node)
  node.tick = function(value)
    result = {}
    result.loop = nil
    result.leave = nil
    if value.initial > value.val then
      result.loop = value.val
    else
      result.leave = value.val
    end
    return result
  end
end

function myNode.spec(node)
  node.name = "While greater"
  node.inputs.val = "Number"
  node.inputs.initial = "Number"
  node.outputs.loop = "Number"
  node.outputs.leave = "Number"
  node.desc = "Loop while initial is greater than val."
end

return myNode
