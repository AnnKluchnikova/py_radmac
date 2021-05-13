from oui_request import get_path_to_OUI_db
import os.path as os_path
import json

def _get_oui_base(log):
# 
  file_path = get_path_to_OUI_db(log)

  if file_path is None:
    return None

  with open(file_path, "r") as read_file:
    return json.load(read_file) # <class 'list'>
# 

def _get_mac_base():
# 
  file_path = "RADMAC_DB.json"

  try:
  # 
    with open(file_path, "r") as read_file:
      data = json.load(read_file) # <class 'list'>

    if data is None:
      return list(), file_path
    else:
      return data, file_path
  # 
  except FileNotFoundError:
  # 
    with open(file_path, "w"):
    # 
      print("[WARNING] The file \"{}\" was not found. \n"
            "          It will be created in the current folder."\
            .format(file_path))
    # 

      return list(), file_path
  # 
  except json.decoder.JSONDecodeError:
  # 
    path = os_path.join(os_path.abspath(os_path.dirname(__file__)), file_path)
    print("[WARNING] Failed to read MAC address database\n"
          "          from file \"{}.\"\n"
          "          The file will be used to store the new database."\
          .format(path))

    return list(), file_path
  # 
# 

def _save_mac_base(data_base, file_path):
# 
  with open(file_path, "w") as write_file:
    json.dump(data_base, write_file, indent=2)
# 

# ==============================================================================

def debag_json_print(body):
# 
  return json.dumps(body, indent = 2)
# 