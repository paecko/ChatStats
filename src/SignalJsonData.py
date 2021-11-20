import subprocess
import json
import io


class SignalJsonData:
    def __new__(cls, sqlite_path, config_path, create_json_file=False):
        json_str_in_bytes = subprocess.check_output(["sh", "./sqlite-to-json.sh", sqlite_path, config_path])
        json_obj = json.load(io.BytesIO(json_str_in_bytes))
        return json_obj
