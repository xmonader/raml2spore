package.loaded['socket'] = nil

local pretty = require 'pl.pretty'
local function slurp(path)
    print(path)
    local f = io.open(path)
    local s = f:read("*a")
    f:close()
    return s
end
local Spore = require 'Spore'

local defs = slurp("todoapi.json")
local todo = Spore.new_from_string(defs)

todo:enable 'Format.JSON'
pretty.dump(todo)

local res = todo:ListTodos()
pretty.dump(res)

local res = todo:UpdateTodo{id=1, payload={title="oufff!", done=false}}
pretty.dump(res.body)


local res = todo:GetTodo({id=1})
if res.status == 200 then   
    pretty.dump(res.body)
end
