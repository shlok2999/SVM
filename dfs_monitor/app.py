import json
from flask import Flask, jsonify, request
from config import DevelopmentConfig
from pymongo import MongoClient
from database_ops import *
from helper import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

mongo_client = MongoClient(app.config['MONGO_URL'])
db = mongo_client.get_database(app.config['MONGO_DB'])
environment_details = get_environment_details()


@app.route('/send_usage')
def send_overall_usage():
    '''
    This functionn is called when the node manager starts running
    It send how much resource is being used in each node
    By fetching details from the db
    '''
    running_config_list = get_config_details(db_obj = db, collection = 'deployments', status = PROVISION_SUCCESS_CODE)
    pending_config_list = get_config_details(db_obj = db, collection = 'deployments', status = PROVISION_PENDING_CODE)

    final_list = running_config_list + pending_config_list

    response = dict()

    for i in final_list:
        config_id = i['config_id']
        topic = i['topic']
        if topic not in response.keys():
            response[topic] = {'ram' : 0,
                                 'cpu' : 0,
                                 'gpu' : 0,
                                 'storage': 0}
        resource = get_resource_detail(db_obj = db, config_id = config_id, collection = 'configs')
        print(resource)
        response[topic]['ram'] += resource['ram']
        response[topic]['gpu'] += resource['gpu']
        response[topic]['cpu'] += resource['cpu']
        response[topic]['storage'] += resource['storage']
    print(response)
    return jsonify(response)

@app.route('/topic_usage')
def send_topic_usage():
    data = request.args.to_dict()
    topic = data['topic']
    running_config_list = get_config_details_by_topic(db_obj = db, collection = 'deployments', status = PROVISION_SUCCESS_CODE, topic = topic)
    pending_config_list = get_config_details_by_topic(db_obj = db, collection = 'deployments', status = PROVISION_PENDING_CODE, topic = topic)

    final_list = running_config_list + pending_config_list
    response = dict()
    ram = 0
    cpu = 0
    gpu = 0
    storage = 0

    for i in final_list:
        config_id = i['config_id']
        resource = get_resource_detail(db_obj = db, config_id = config_id, collection = 'configs')
        ram += resource['ram']
        gpu += resource['gpu']
        cpu += resource['cpu']
        storage += resource['storage']
    
    response['ram'] = ram
    response['gpu'] = gpu
    response['cpu'] = cpu
    response['storage'] = storage

    return response


@app.route('/add_container',methods = ['GET','POST'])
def add_container_details():
    '''
    Set the status of the container to the pending state
    '''
    data = request.json
    save_deployment_detail(db_obj = db, topic = data['topic'], collection = 'deployments', config_data = data, node_agent_id= 'node-agent_' + data['topic'])
    return jsonify({'status':200})

@app.route('/update_status',methods = ['GET','POST'])
def update_container():
    '''
    Updates the status of container in the db
    Sends an update to node manger regarding the same
    '''
    data = request.json
    update_deployment_detail(db_obj = db, config_id = data['config_id'], collection = 'deployments', status = data['status'])
    if data['status'] == PROVISION_FAILURE_CODE:
        response = get_resource_detail(db_obj = db, config_id = data['config_id'], collection = 'configs')
        post_response(ip = environment_details['node_manager'], function = '/node_failed', data = response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8020, debug=True)