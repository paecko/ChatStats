import subprocess
import json


class SignalJsonMessages:
    def __new__(cls, sqlite_path, config_path, create_json_file=False):
        json_str_in_bytes = subprocess.check_output(["sh", "./sqlite-to-json.sh", sqlite_path, config_path])
        json_str_list = json.loads(json_str_in_bytes)
        # last item in returned list is an empty string so we remove it.
        if len(json_str_list) > 0:
            json_str_list.pop()
        json_message_objects = []

        for message in json_str_list:
            json_message_objects.append(json.loads(message))

        return json_message_objects
