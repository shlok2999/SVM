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
import public_ip as ip
from flask_cors import CORS


logging.basicConfig(filename='record.log', 
                    level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
CORS(app)

mongo_client = MongoClient(app.config['MONGO_URL'])
db = mongo_client.get_database(app.config['MONGO_DB'])


@app.route("/config", methods=["POST"])
def get_env_config():
    user_config_contract = request.get_json()
    print(user_config_contract)
    
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
                app.logger.error(f"db operation failed for os ")
                return create_response(INTERNAL_SERVER_ERROR), 500

            # node_manager_url = get_node_manager(db_object)
            # ans = get_response(f'{node_manager_url}/node_info',data['resources'])
            # kafka_producer_obj = Kafka_Producer(ans['topic'])
            # kafka_producer_obj.send_valid_config(data)
            app.logger.info(f"no entry found in db for os ")
            return create_response(VALID_CONFIG), 200
        
        app.logger.error(f"no entry found in db for os ")
        return create_response(INVALID_CONFIG), 403
    
    app.logger.error(f"no entry found in db for os ")
    return create_response(INVALID_CONFIG), 403


@app.route("/library/os")
def get_os_names():
    app.logger.info(f"received request for get_library_detail()")
    library_obj = get_os_list(db, app.config['LIBRARY_COLL'])

    if library_obj is None:
        app.logger.error(f"failed to query db or no entry found in db for library collection")
        return create_response(INTERNAL_SERVER_ERROR), 500

    if len(library_obj.keys()) == 0:
        app.logger.error(f"no entry found in db")
        return create_response(INVALID_LIBRARY), 403

    app.logger.info(f"returning entries for all operating system present in library")
    
    return library_obj, 200


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

def register_self():
    self_ip_addr = get_local_ip()
    if app.config['DEVELOPMENT'] == False:
        self_ip_addr = ip.get()

    app.logger.info(f"registering service {app.config['DFS_SERVER']} at ip {self_ip_addr}")

    free_port = next_free_port()

    if free_port is None:
        raise ValueError('could not find a free port')
    
    app.logger.info(f"found free port at {free_port}")
    
    if not register_service(db, app.config['SERVICES_COLL'], 
                            app.config['DFS_SERVER'], 
                            self_ip_addr, free_port):
        raise Exception('could not register service')

    app.logger.info(f"registering service {app.config['DFS_SERVER']} at ip {self_ip_addr} and port {free_port}")

    return self_ip_addr, free_port

@app.route("/configs")
def retrieve_all_configs():
    app.logger.info(f"received request for retireieve_all_configs()")
    configs_obj = get_all_configs(db, app.config['CONFIGS_COLL'], app.config['DEPLOYMENTS_COLL'])

    if configs_obj is None:
        app.logger.error(f"failed to query db or No entry found in db for configs collection")
        return create_response(INTERNAL_SERVER_ERROR), 500

    app.logger.info(f"returning all configs list from db")
    return create_bson_response(configs_obj)


@app.route("/deployments")
def retrieve_all_deployments():
    app.logger.info(f"received request for retireieve_all_deployments()")
    deployments_obj = get_all_deployments(db, app.config['DEPLOYMENTS_COLL'])

    if deployments_obj is None:
        app.logger.error(f"failed to query db or No entry found in db for deployments collection")
        return create_response(INTERNAL_SERVER_ERROR), 500

    app.logger.info(f"returning all deployments list from db")
    return create_bson_response(deployments_obj)

@app.route("/configs/<config_id>")
def get_single_config(config_id):
    app.logger.info(f"received request for get_single_config() for config id {config_id}")
    config_obj = get_config(db, app.config['CONFIGS_COLL'], config_id)

    if config_obj is None:
        app.logger.error(f"failed to query db or No entry found in db for configs collection for config id {config_id}")
        return create_response(INTERNAL_SERVER_ERROR), 500

    app.logger.info(f"returning record for config id {config_id} from db")
    return create_bson_response(config_obj)

@app.route("/deployment/<config_id>")
def get_single_deployment_status(config_id):
    app.logger.info(f"received request for get_single_deployment() for config id {config_id}")
    deployment_status = get_deployment_status(db, app.config['DEPLOYMENTS_COLL'], config_id)

    app.logger.info(f"returning record for config id {config_id} from db")
    return jsonify(deployment_status)

@app.route("/provision/<config_id>", methods=["POST"])
def provision_env(config_id):
    config_obj = get_config(db, app.config['CONFIGS_COLL'], config_id)
    
    if config_obj is None:
        app.logger.error(f"failed to query db or No entry found in db for configs collection for config id {config_id}")
        return create_response(INTERNAL_SERVER_ERROR), 500
    
    node_manager_address = get_node_manager(db, app.config['SERVICES_COLL'], app.config['NODE_MANAGER'])
    if node_manager_address == None:
        app.logger.error(f"could not find noide manager address")
        return create_response(INTERNAL_SERVER_ERROR), 500
    
    request_stub = {}
    request_stub['resources'] = config_obj['resources']
    request_stub['env_name'] = config_obj["env-name"]
    request_stub['_id'] = str(config_obj['_id'])
    request_stub['storage'] = config_obj['storage']
    deployable_node = post_response(node_manager_address, app.config["NODE_MANAGER_NODE_INFO_API"], request_stub)
    print(deployable_node)
    if deployable_node['resource_available'] == False:
        app.logger.error(f"failed to find enough free resources for config id {config_id}")
        return create_response(INTERNAL_SERVER_ERROR), 500

    # node_agent_id = f'node-agent_{deployable_node['topic']}'
    # deployment_id = save_deployment_detail(db, app.config['DEPLOYMENTS_COLL'], 
    #                                     config_id, node_agent_id)
    
    # if deployment_id is None:
    #     app.logger.error(f"could not find noide manager address")
    #     return create_response(INTERNAL_SERVER_ERROR), 500
    
    # config_obj[0]['deployment_id'] = deployment_id
    
    kafka_producer_obj = Kafka_Producer(deployable_node['topic'])
    config_obj_data = config_obj
    del config_obj_data['creation_time']
    del config_obj_data['last_updation_time']
    config_obj_data['_id'] = str(config_obj_data['_id'])
    print(config_obj_data)
    kafka_producer_obj.send_valid_config(config_obj_data)
    return jsonify({'status':200})

if __name__ == "__main__":
    ip, port = register_self()
    app.run(host=ip, port=port, debug=False)