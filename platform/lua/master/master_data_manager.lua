local master_data = require(object.path .. ".master_data")

local master_data_manager = {}

master_data_manager.new = function (data_name)
    local obj = {}
    setmetatable(obj, {__index = master_data_manager})
    obj.data_list = obj:convert_csv("master/" .. data_name .. ".csv")
    return obj
end

master_data_manager.getData = function (self, id)
    return self.data_list[id]
end

master_data_manager.setData = function (self, id, data)
    self.data_list[id] = data
end

master_data_manager.find = function (self, f)
    local ret = {}

    for _, data in pairs(self.data_list) do
        if f(data) then
            table.insert(ret, data)
        end
    end

    return ret
end

master_data_manager.convert_csv = function (self, path)
    local f = assert(io.open(path))
    local csv = f:read("*all")
    self.data_list = self:convert_csv_str(csv)
    f:close()
end

master_data_manager.convert_csv_str = function (self, csv)
    local items = {}                      
    local headers = {}                    
    local first = true
    for line in csv:gmatch("[^\n]+") do
        if first then                       
            -- ヘッダ読み込み
            local count = 1
            for header in line:gmatch("[^,]+") do 
                headers[count] = header
                count = count + 1
            end
            first = false                    
        else
            -- データ読み込み
            local i = 1                       
            local data = setmetatable({}, {__index = master_data})
            data = master_data.new()
            for field in line:gmatch("[^,]+") do
                data[headers[i]] = field
            end
            if data["Id"] ~= nil then
                items[data["Id"]] = data
            end
        end
    end
    return items
end

return master_data_manager