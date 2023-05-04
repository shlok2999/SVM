import json
import datetime
# from flask_pymongo import PyMongo
import pymongo
from constants import *
from bson.objectid import ObjectId


def create_stub_for_one_lang(language_name, lang_record):
    temp_stub = {}
    temp_stub["name"] = language_name
    temp_stub["libraries"] = list(lang_record.keys())

    return temp_stub


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
        config_record = list(col_obj.find({"_id": ObjectId(config_id)}))
        return config_record
    except Exception as e:
        print("An exception occurred ::", e)
        return None

def save_deployment_detail(db_obj, collection, config_data, topic, node_agent_id):
    deployment_obj = {}
    try:
        col_obj = db_obj[collection]
        deployment_obj['config_id'] = ObjectId(config_data['_id'])
        deployment_obj['node_agent_id'] = node_agent_id
        deployment_obj['status'] = PROVISION_PENDING_CODE
        deployment_obj['last_deployment_time'] = datetime.datetime.utcnow()
        deployment_obj['is_active'] = 1
        deployment_obj['topic'] = topic
        col_obj.insert_one(deployment_obj)

        return deployment_obj.inserted_id
    except Exception as e:
        print("An exception occurred ::", e)
        return None


def update_deployment_detail(db_obj, config_id, collection, status):
    if isinstance(config_id,str):
        config_id = ObjectId(config_id)
    myquery = { "config_id": config_id }
    newvalues = { "$set": { "status": status } }
    try:
        col_obj = db_obj[collection]
        col_obj.update_many(myquery, newvalues)
        return 0
    except Exception as e:
        print("An exception occured",e)
        return None


def get_resource_detail(db_obj, config_id, collection):
    if isinstance(config_id,str):
        config_id = ObjectId(config_id)
    myquery = {"_id": config_id}
    try:
        col_obj = db_obj[collection]
        data = col_obj.find_one(myquery)
        print(data)
        resource_data = data['resources']
        storage = 0
        resource_data['ram'] = float(resource_data['ram'][:-1])
        resource_data['cpu'] = float(resource_data['cpu'])
        resource_data['gpu'] = int(resource_data['gpu'])
        for s in data['storage']:
            size = s['size'][:-1]
            size = float(size)
            storage += size
        resource_data['storage'] = storage
        resource_data['container_name'] = data["env-name"]
        return resource_data
    except Exception as e:
        print("An exception occured",e)
        return None


def get_config_details(db_obj, collection, status):
    myquery = {"status": status}
    try:
        col_obj = db_obj[collection]
        response = [ i for i in col_obj.find(myquery)]
        return response
    except Exception as e:
        print("An exception occured",e)
        return []

def get_config_details_by_topic(db_obj, collection, topic, status):
    myquery = {"topic": topic, "status":status}
    try:
        col_obj = db_obj[collection]
        response = [ i for i in col_obj.find(myquery)]
        return response
    except Exception as e:
        print("An exception occured",e)
        return []

def get_service(db_obj, collection, service_name):
    try:
        col_obj = db_obj[collection]
        service = col_obj.find_one({"service-name": service_name})
        return f'{service["ip"]:{service["port"]}}'
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

def get_config_status(db_obj,collection,config_id):
    # print(type(config_id))
    config_id = ObjectId(config_id)
    myquery = {'config_id' : config_id}
    try:
        col_obj = db_obj[collection]
        # print("connected")
        result = col_obj.find_one(myquery)
        # print(result)
        return {'status':result['status']}
    except Exception as e:
        print("An exception occurred ::", e)
        return {'status':-1}