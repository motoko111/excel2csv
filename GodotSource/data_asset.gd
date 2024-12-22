class_name DataAsset

static var s_instance = null
var master = {}

static func getInstance():
	if s_instance == null:
		s_instance = DataAsset.new()
	return s_instance

static func register(dataName, data):
	getInstance().master[dataName]= data

static func clear():
	getInstance().master = {}
	
static func loadAll():
	var files = FileUtils.getFiles("res://src/master/data")
	for file:String in files:
		DataAsset.getData(file.replace(".gd",""))
	
static func _createDataInstance(dataName):
	var class_ref = load("res://src/master/data/"+ dataName + ".gd")
	var data = class_ref.getInstance()
	if data :
		register(dataName, data)

static func getData(dataName):
	if !getInstance().master.has(dataName):
		_createDataInstance(dataName)
	return getInstance().master[dataName]

static func getRecords(dataName):
	return getData(dataName).getRecords()
	
static func getNameMapRecords(dataName):
	return getData(dataName).getNameMapRecords()

static func getIdMapRecords(dataName):
	return getData(dataName).getIdMapRecords()

static func getFields(dataName):
	return getData(dataName).getFields()

static func findById(dataName,id):
	return getData(dataName).findById(id)

static func findByName(dataName,name):
	return getData(dataName).findByName(name)

static func getDataMaster():
	return getInstance().master
