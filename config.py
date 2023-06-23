import json
import os

json_file = 'config.json'

def write_config(dict: dict):
    with open(json_file, 'w') as jsonfile:
        try:
            json.dump(dict, jsonfile)
            return True
        except Exception as e:
            return False

def read_config():
    with open(json_file, 'r') as jsonfile:
        try:
            data = json.loads(jsonfile.read())
            return data
        except Exception as e:
            return False

def update_config(key: str, value: str):
    data = read_config()
    try:
        data[key] = value

        write_config(data)
    except KeyError as e:
        return False

def get_value(key: str):
    data = read_config()
    try:
        return data[key]
    except KeyError as e:
        return False

def create_basic(default_cheat):
    write_config({'cheat': default_cheat})
def init(default_cheat):
    if not os.path.isfile(json_file):
        create_basic(default_cheat)
    elif not read_config():
        create_basic(default_cheat)