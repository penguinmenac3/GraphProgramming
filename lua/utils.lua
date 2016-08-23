local myUtils = {}
-- Utils for graphex

function myUtils.scandir(directory)
  local i, t, popen = 0, {}, io.popen
  local pfile = popen('ls -a "'..directory..'"')
  for filename in pfile:lines() do
    if not (filename == ".") and not (filename == "..") then
      i = i + 1
      t[i] = filename
    end
  end
  pfile:close()
  return t
end

myUtils.List = {}
function myUtils.List.new ()
  return {first = 0, last = -1}
end

function myUtils.List.pushleft(list, value)
  local first = list.first - 1
  list.first = first
  list[first] = value
end

function myUtils.List.pushright(list, value)
  local last = list.last + 1
  list.last = last
  list[last] = value
end

function myUtils.List.popleft(list)
  local first = list.first
  if first > list.last then error("list is empty") end
  local value = list[first]
  list[first] = nil
  list.first = first + 1
  return value
end

function myUtils.List.popright(list)
  local last = list.last
  if list.first > last then error("list is empty") end
  local value = list[last]
  list[last] = nil
  list.last = last - 1
  return value
end

function myUtils.List.length(list)
  return list.last - list.first + 1
end

function myUtils.List.empty(list)
  return list.first > list.last
end

return myUtils
