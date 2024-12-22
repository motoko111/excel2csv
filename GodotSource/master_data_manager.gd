class_name MasterDataManager

var nameMap = {}
var idMap = {}
var groupIdMap = {}
var dataName = ""
var fields = {}
var records = {}

func _init():
	DataAsset.register(dataName, self)
	for record in records:
		if record.has("name"):
			nameMap[record.name] = record
		if record.has("id"):
			idMap[record.id] = record
		if record.has("group_id"):
			if !groupIdMap.has(record.group_id):
				groupIdMap[record.group_id] = []
			groupIdMap[record.group_id].append(record)

func getRecords():
	return records
	
func getNameMapRecords():
	return nameMap

func getIdMapRecords():
	return idMap
	
func getGroupIdMapRecords():
	return groupIdMap
	
func findByGroupId(groupId):
	if groupIdMap.has(groupId):
		return groupIdMap[groupId]
	return []

func getFields():
	return fields

func findById(id):
	return idMap[id]

func findByName(name):
	return nameMap[name]
