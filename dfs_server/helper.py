import requests
import json
import socket
from flask import jsonify
import json
import jsonschema
from jsonschema import validate
import bson.json_util as json_util
from requests import get

def get_schema():
    with open('config_schema.json', 'r') as file:
        schema = json.load(file)
    return schema


def validate_config_structure(json_data):
    with open('dfs_contract.json', 'r') as f:
        jsonData = json.load(f)
    
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    
    return True

def validate_config_entries(library_obj, user_config_contract):
    if library_obj == None and len(library_obj.keys()) == 0:
        return False
    
    user_language_choice = {}

    for language in user_config_contract['languages']:
        user_language_choice[language['language-name']] = language['libraries']

    for obj in library_obj["languages"]:
        lang_name = obj["name"]
        libraries_list_from_library = obj["libraries"]
        if lang_name in user_language_choice:
            diff = list(set(user_language_choice[lang_name]) - set(libraries_list_from_library))
            if len(diff) > 0:
                return False
    
    return True

def create_response(message):
    return jsonify({"response": message})

def create_bson_response(message):
    return json_util.dumps({"response": message})


def get_response(ip_address,data):
    ans = requests.get(ip_address, params=data).content.decode()
    ans = json.loads(ans)
    return ans

def post_response(ip_address,function,data):
    ans = requests.post(ip_address + function, json=data).json()
    # ans = json.loads(ans)
    return ans


def get_environment_details():
    file_desc = open('environment.json')
    data = json.load(file_desc)
    file_desc.close()
    return data

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        self_ip = s.getsockname()[0]
    except Exception:
        self_ip = '127.0.0.1'
    finally:
        s.close()

    print(self_ip)
    return self_ip

def next_free_port():
    port = 8000
    max_port = 65536
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    return None
