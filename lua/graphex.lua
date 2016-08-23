----------------------------------------------------------------------------
-- The Graphexecution environment in LUA
--
-- Author: Michael Fürst (mail@michaelfuerst.de)
-- LICENSE: TODO (Not public yet)
----------------------------------------------------------------------------

local json = require("json")
local utils = require("utils")

debug = nil
global_args = {}
offset = 2

if not (arg[2] == nil) then
  if arg[2] == "debug" then
    debug = require("debugger")
    offset = 3
  end
end

local tmp_args = ""
local tmp_args_bool = false
while not (arg[offset] == nil)
do
  tmp_args_bool = true
  tmp_args = tmp_args .. arg[offset] .. " "
  offset = offset + 1
end

if tmp_args_bool then
  global_args = json.decode(tmp_args)
end

global_result = {}

-- Load the graph as a table.
function loadGraph(filename)
  file = io.open(filename, "r")
  local graph_txt = file:read("*a")
  file:close()
  --print(graph_txt)
  return json.decode(graph_txt)
end

function buildGraph(graph)
  -- Initialize variables
  local nodes = {}
  local inputNodes = {}

  -- Create nodes
  for key, value in ipairs(graph.nodes)
  do
    local tmp = require(value.code)
    tmp.init(value)
    nodes[value.name] = value
    value.running = false
    value.heat = 0
    if value["queue_enabled"] == nil then
      value.queue_enabled = true
    end

    value.is_input = true
    for p in pairs(value.inputs)
    do
      value.inputs[p] = utils.List.new()
      value.is_input = false
    end
    if value.is_input == true then
      inputNodes[value.name] = value
    end
  end

  -- Create Connections
  for key, value in ipairs(graph.connections)
  do
    nodes[value.input.node].outputs[value.input.output] = value.output
  end

  return nodes, inputNodes
end

function runGraph(graph, inputNodes)
  local pendingForSchedule = utils.List.new()
  for x in pairs(inputNodes)
  do
    utils.List.pushright(pendingForSchedule, x)
  end

  while not utils.List.empty(pendingForSchedule)
  do
    --print(utils.List.length(pendingForSchedule))
    --print(json.encode(pendingForSchedule))
    local current_id = utils.List.popleft(pendingForSchedule)
    local current = graph[current_id]
    local value = {}
    
    -- Check if all inputs are availible and abort if not.
    for k in pairs(current.inputs)
    do
      --print(json.encode(current.inputs[k]))
      if utils.List.empty(current.inputs[k]) then
        value = nil
        break
      end
    end
    if value == nil then
      --utils.List.pushright(pendingForSchedule, current_id)
    else
      -- Gather inputs from queue
      for k in pairs(current.inputs)
      do
        if current.queue_enabled == false then
          while utils.List.length(current.inputs[k]) > 1
          do
            utils.List.popleft(current.inputs[k])
          end
        end
        value[k] = utils.List.popleft(current.inputs[k])
      end

      local result = current.tick(value)
      for output in pairs(current.outputs)
      do
        if not (result[output] == nil) then
          utils.List.pushright(graph[current.outputs[output].node].inputs[current.outputs[output].input], result[output])
          utils.List.pushright(pendingForSchedule, current.outputs[output].node)
        end
      end
    end
  end
end

local tmp = loadGraph(arg[1])
local graph, inputNodes = buildGraph(tmp)
runGraph(graph, inputNodes)
print(json.encode(global_result))
