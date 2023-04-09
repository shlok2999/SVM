import requests
import json

from flask import jsonify
import json
import jsonschema
from jsonschema import validate
import bson.json_util as json_util


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
    
def get_environment_details():
    file_desc = open('environment.json')
    data = json.load(file_desc)
    file_desc.close()
    return data