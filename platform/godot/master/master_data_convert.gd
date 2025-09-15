@tool
class_name MasterDataConverter
extends EditorScript

func _run():
	print("============================== MasterDataConverter run start ==============================")
	var output = []
	var project_path = ProjectSettings.globalize_path("res://")
	var batch_path = project_path + "batch/export_data.bat"
	print("execute batch:" + batch_path)
	var exit_code = OS.execute(batch_path, [], output)
	print("result:\n" + str(output))
	print("============================== MasterDataConverter run end ==============================")
