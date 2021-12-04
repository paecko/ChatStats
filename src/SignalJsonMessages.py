import subprocess
import json


class SignalJsonMessages:

    def __new__(cls, config_to_sqlite_paths: dict, create_json_file=False):
        json_message_objects = []
        for config, sqlite in config_to_sqlite_paths.items():
            SignalJsonMessages.run_sqlite_to_json_script(config, sqlite, json_message_objects)

        if create_json_file:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(json_message_objects, f, ensure_ascii=False, indent=4)
                
        return json_message_objects

    @classmethod
    def run_sqlite_to_json_script(cls, config_path, sqlite_path, json_message_objects):
        json_str_in_bytes = subprocess.check_output(["sh", "./sqlite-to-json.sh", sqlite_path, config_path])
        json_str_list = json.loads(json_str_in_bytes)
        # last item in returned list is an empty string so we remove it.
        if len(json_str_list) > 0:
            json_str_list.pop()
        for message in json_str_list:
            json_message_objects.append(json.loads(message))
