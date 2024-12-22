local master_data = {}

master_data.new = function ()
    local obj = {}
    obj.Id = ""
    obj.Name = ""
    return setmetatable(obj, {__index = master_data})
end

return master_data