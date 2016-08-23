-- Build the nodespec for lua

local json = require('json')
local utils = require('utils')

function createSpecForNode(code)
  print("Create spec for " .. code)
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

function findNodesIn(directory)
  nodeList = {}
  i = 0
  tmp = utils.scandir(directory)
  for x in pairs(tmp)
  do
    res = utils.scandir(directory.."/"..tmp[x])
    for y in pairs(res)
    do
      i = i + 1
      nodeList[i] = directory.."."..tmp[x].."."..res[y].gsub(res[y], ".lua", "")
    end
  end
  return nodeList
end

local tmp = findNodesIn("stdlib")
local nodeSpecList = createNodeSpecList(tmp)
writeNodeSpecList(nodeSpecList, "../grapheditor/data/Lua.nodes.json")
