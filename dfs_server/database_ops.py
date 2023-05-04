import json
import datetime
# from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket

def create_stub_for_one_lang(language_name, lang_record):
    temp_stub = {}
    temp_stub["name"] = language_name
    temp_stub["libraries"] = list(lang_record.keys())

    return temp_stub


def get_os_list(db_obj, collection):
    col_obj = db_obj[collection]

    library_json_stub = {}
    try:
        library_records = col_obj.find({})
        library_json_stub["os-list"] = []

        for record in library_records:
            library_json_stub["os-list"].append(record['os'])

        return library_json_stub
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def get_library(db_obj, collection, os_name):
    col_obj = db_obj[collection]

    library_json_stub = {}
    try:
        library_records = col_obj.find({"os": os_name})
        if len(list(library_records.clone())) == 0:
            return library_json_stub
        
        library_json_stub["os"] = os_name
        library_json_stub["languages"] = []
        for record in library_records:
            for language in record["specifications"]:
                libraries_list = record["specifications"][language]["libraries"]
                temp_language_stub = create_stub_for_one_lang(language, libraries_list)
                library_json_stub["languages"].append(temp_language_stub)
            
        return library_json_stub
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def save_in_db(db_obj, collection, data):
    try:
        data['is_active'] = 1
        data['creation_time'] = datetime.datetime.utcnow()
        data['last_updation_time'] = datetime.datetime.utcnow()
        col_obj = db_obj[collection]
        col_obj.insert_one(data)
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def get_all_templates(db_obj, collection):
    try:
        col_obj = db_obj[collection]
        template_records = list(col_obj.find())
        return template_records
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def get_template(db_obj, collection, template_id):
    try:
        col_obj = db_obj[collection]
        template_records = list(col_obj.find({"_id": ObjectId(template_id)}))
        return template_records
    except Exception as e:
        print("An exception occurred ::", e)
        return None


def get_config(db_obj, collection, config_id):
    try:
        col_obj = db_obj[collection]
        config_record = col_obj.find_one({"_id": ObjectId(config_id)})
        return config_record
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def save_deployment_detail(db_obj, collection, config_id, node_agent_id):
    deployment_obj = {}
    try:
        col_obj = db_obj[collection]
        deployment_obj['config_id'] = config_id
        deployment_obj['node_agent_id'] = node_agent_id
        deployment_obj['status'] = PROVISION_PENDING_CODE
        deployment_obj['last_deployment_time'] = datetime.datetime.utcnow()
        deployment_obj['is_active'] = 1
        col_obj.insert_one(deployment_obj)

        return deployment_obj.inserted_id
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def get_all_configs(db_obj, collection):
    try:
        col_obj = db_obj[collection]
        config_record = list(col_obj.find({}))
        return config_record
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def register_service(db_obj, collection, service_name, ip, port):
    try:
        col_obj = db_obj[collection]
        final_ip_address = f'http://{ip}'
        col_obj.update_one({"service-name" : service_name},{"$set": { "ip" : final_ip_address, "port": port}}, upsert=True)
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False

def get_node_manager(db_obj, collection, service_name):
    try:
        col_obj = db_obj[collection]
        node_manager = col_obj.find_one({"service-name": service_name})
        return f'{node_manager["ip"]}:{node_manager["port"]}'
    except Exception as e:
        print("An exception occurred ::", e)
        return None