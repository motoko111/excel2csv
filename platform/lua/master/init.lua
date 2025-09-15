master = {
    path = ...
}
master.master_data_manager = require(master.path .. ".master_data_manager")
master.master_data = require(master.path .. ".master_data")

return master