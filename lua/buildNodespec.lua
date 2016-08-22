-- Build the nodespec for lua

local json = require('json')
local utils = require('utils')

function createSpecForNode(code)
  -- Create and prepopulate node spec
  node = {}
  node.name = "Specify Node Name"
  node.code = code
  node.inputs = {}
  node.outputs = {}
  node.args = {}
  node.desc = "Specify a node description (desc)"

  -- load and populate spec by node
  local tmp = require(code)
  tmp.spec(node)

  return node
end

function createNodeSpecList(nodeList)
  local nodeSpecList = {}
  local index = 1
  for k in pairs(nodeList)
  do
    nodeSpecList[index] = createSpecForNode(nodeList[k])
    index = index + 1
  end
  return nodeSpecList
end

function writeNodeSpecList(nodeSpecList, filename)
  file = io.open(filename, "w")
  file:write(json.encode(nodeSpecList))
  file:close()
end

local tmp = {"stdlib.system.print", "stdlib.string.const", "stdlib.string.concat"}
local nodeSpecList = createNodeSpecList(tmp)
writeNodeSpecList(nodeSpecList, "../grapheditor/data/Lua.nodes.json")
