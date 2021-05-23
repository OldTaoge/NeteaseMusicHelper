import json

_config_data = None
_method = "file"
_path = ""


def Data_NemData(method="file", path=""):
    global _method
    global _path

    _method = method
    _path = path
    global _config_data
    if _method == "file" and _config_data is None:
        with open(_path, "r") as config_file:
            _config_data = json.load(config_file)


def Data_getData():
    return _config_data


def Data_saveData():
    global _path
    if _method == "file" and _config_data["config"]["config"]["write"]:
        with open(_path, "w") as config_file:
            json.dump(_config_data, config_file, indent=4)
