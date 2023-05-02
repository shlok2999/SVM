import json
from flask import Flask, jsonify, request
from kafka_producer import Kafka_Producer
from helper import *
from config import DevelopmentConfig
from pymongo import MongoClient
from database_ops import *
from constants import *
import bson.json_util as json_util
import logging

logging.basicConfig(filename='record.log', 
                    level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

mongo_client = MongoClient(app.config['MONGO_URL'])
db = mongo_client.get_database(app.config['MONGO_DB'])


@app.route("/config", methods=["POST"])
def get_env_config():
<<<<<<< Updated upstream
    user_config_contract = request.get_json()
    
    app.logger.info(f"received request for get_env_config()")
    
    if "isTemplate" in user_config_contract and user_config_contract["isTemplate"] == 1:
        if "template-id" not in user_config_contract:
            app.logger.error(f"invalid config. missing tempalte-id entry")
            return create_response(INVALID_CONFIG), 403
        
        template_id = user_config_contract["template-id"]
        app.logger.info(f"found template-id {template_id} in config")

        template_obj = get_template(db, app.config['TEMPLATES_COLL'], template_id)
        
        if template_obj is not None:
            if len(template_obj) > 0:
                for obj in template_obj:
                    user_config_contract['os'] = obj['os']
                    user_config_contract['languages'] = obj['languages']
                    user_config_contract['resources'] = obj['resources']
            else:
                app.logger.error(f"couldnt find entry for template {template_id} in db")
                return create_response(INVALID_CONFIG), 403
        else:
            app.logger.error(f"failed to query db or record doesnt exist for template-id {template_id}")
            return create_response(INTERNAL_SERVER_ERROR), 500                

    if validate_config_structure(user_config_contract):
        library_obj =  get_library(db, app.config['LIBRARY_COLL'], user_config_contract["os"])
        if validate_config_entries(library_obj, user_config_contract):
            if not save_in_db(db, app.config['CONFIGS_COLL'], user_config_contract):
                app.logger.error(f"db operation failed for os {os_name}")
                return create_response(INTERNAL_SERVER_ERROR), 500

            # node_manager_url = get_node_manager(db_object)
            # ans = get_response(f'{node_manager_url}/node_info',data['resources'])
            # kafka_producer_obj = Kafka_Producer(ans['topic'])
            # kafka_producer_obj.send_valid_config(data)
            app.logger.info(f"no entry found in db for os {os_name}")
            return create_response(VALID_CONFIG), 200
        
        app.logger.error(f"no entry found in db for os {os_name}")
        return create_response(INVALID_CONFIG), 403
    
    app.logger.error(f"no entry found in db for os {os_name}")
    return create_response(INVALID_CONFIG), 403

@app.route("/library/os/<os_name>")
def get_library_detail(os_name):
    app.logger.info(f"received request for get_library_detail()")
    library_obj = get_library(db, app.config['LIBRARY_COLL'], os_name)

    if library_obj is None:
        app.logger.error(f"failed to query db or no entry found in db for library collection")
        return create_response(INTERNAL_SERVER_ERROR), 500

    if len(library_obj.keys()) == 0:
        app.logger.error(f"no entry found in db for os {os_name}")
        return create_response(INVALID_LIBRARY), 403

    app.logger.info(f"returning entries in db for os {os_name}")
    return library_obj, 200

@app.route("/templates")
def get_templates():
    app.logger.info(f"received request for get_templates()")
    templates_obj = get_all_templates(db, app.config['TEMPLATES_COLL'])

    if templates_obj is None:
        app.logger.error(f"failed to query db or No entry found in db for templates collection")
        return create_response(INTERNAL_SERVER_ERROR), 500

    app.logger.info(f"returning all templates list from db")
    return create_bson_response(templates_obj)

# @app.route("/provision/<config_id>", methods=["POST"])
# def provision_env(config_id):
#     config_obj = get_config(db, app.config['CONFIGS_COLL'], config_id)
    
#     if config_obj is None:
#         return create_response(INTERNAL_SERVER_ERROR), 500
    
#     if len(config_obj) == 0:
#         return create_response(INVALID_CONFIG), 403
    
#     node_manager_obj = get_node_manager(db, app.config['SERVICES_COLL'])
#     if len(node_manager_obj) == 0:
#         return create_response(INTERNAL_SERVER_ERROR), 500
    
#     deployable_node = get_response(f'{node_manager_obj['address']}/node_info',config_obj[0]['resources'])
    
#     deployment_id = save_deployment_detail(db, app.config['DEPLOYMENTS_COLL'], 
#                                         config_obj[0], deployable_node['id'])
    
#     if deployment_id is None:
#         return create_response(INTERNAL_SERVER_ERROR), 500
    
#     config_obj[0]['deployment_id'] = deployment_id
    
#     kafka_producer_obj = Kafka_Producer(node_manager_obj['topic'])
#     kafka_producer_obj.send_valid_config(config_obj)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)