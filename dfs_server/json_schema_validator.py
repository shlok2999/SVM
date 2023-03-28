import json
import jsonschema
from jsonschema import validate

def get_schema():
    with open('config_schema.json', 'r') as file:
        schema = json.load(file)
    return schema


def validate_config(json_data):
    with open('dfs_contract.json', 'r') as f:
        jsonData = json.load(f)
    
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False, err
    
    return True



# is_valid, msg = validate_json(jsonData)
# print(msg)

