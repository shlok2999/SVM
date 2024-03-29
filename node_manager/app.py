import json
from flask import Flask, jsonify, request
from threading import Thread
from helper import *
from config import DevelopmentConfig
import time
import atexit
import socket
from pymongo import MongoClient
from database_ops import *
import bson.json_util as json_util
import logging
import public_ip as ip

cached_status = dict() # Used to store the current free resources in nodes
killed = True
health_thread = None
node_usage_status = dict() # Used to know how much resource of each node is already used
environment_details = get_environment_details()
db = None

def get_health(thread_name,db,config):
    '''
    Fetch IPs from central DB
    And get health of all new Nodes Available
    '''
    global cached_status
    global killed
    print('in get health')
    while(killed):
        node_agents = get_node_agents_list()
        print(node_agents)
        current_status = dict()
        for agent in node_agents:
            node_status_api_path = f'{agent["ip"]}:{agent["port"]}{app.config["NODE_AGENT_STATUS_API"]}'
            topic = None
            try:
                print('sending request to :',agent['ip'])
                response = get_response(node_status_api_path,"",None)
                print('got response',response)
                topic = response['topic']
                print("topic:",topic)
                current_status[response['topic']] = response
                print("current status",current_status)
                if response['topic'] not in node_usage_status:
                    node_monitor_url = get_service(db, config['SERVICES_COLL'], 'node-monitor')
                    node_usage_status[response['topic']] = get_response(node_monitor_url,'/topic_usage',{'topic':response['topic']})
                print("Upadted Successfully")
            except:
                if topic is not None:
                    if topic in node_usage_status.keys():
                        del node_usage_status[topic]
                    if topic in  current_status.keys():
                        del current_status[topic]
        print(current_status)        
        for topic in current_status.keys():
            current_status[topic]['cpu_count'] -= node_usage_status[topic]['cpu']
            current_status[topic]['gpu_count'] -= node_usage_status[topic]['gpu']
            current_status[topic]['free_ram'] -= node_usage_status[topic]['ram']

        cached_status = current_status
        # print(node_usage_status)
        print(cached_status)
        time.sleep(5)


def get_node_agents_list():
    node_agents = get_node_agents(db, app.config['SERVICES_COLL'], app.config['NODE_AGENT_TYPE'])
    return node_agents



def select_node(data,cached_data):
    '''
    This Function is node selection algorithm
    The node is selected on the basis of cached data
    '''
    # print(cached_data)
    # return cached_data[list(cached_data.keys())[0]]
    global cached_status
    response = {}
    response['resource_available'] = False
    response['topic'] = None
    Node = None
    print(cached_data)
    for node in cached_data.keys():
        print(cached_data[node])
        if data['ram'] <= cached_data[node]['free_ram'] and data['cpu'] <= cached_data[node]['cpu_count'] and data['gpu'] <= cached_data[node]['gpu_count'] and data['storage'] <= cached_data[node]['free_disk_space']:
            response['topic'] = cached_data[node]['topic']
            response['resource_available'] = True
            post_data = data
            post_data['topic'] = cached_data[node]['topic']
            node_monitor_url = get_service(db, app.config['SERVICES_COLL'], 'node-monitor')
            post_response(node_monitor_url, app.config['NODE_MONTIOR_ADD_CONTAINER_API'], post_data)

            cached_data[node]['free_ram'] -= data['ram']
            cached_data[node]['gpu_count'] -= data['gpu']
            cached_data[node]['cpu_count'] -= data['cpu']
            cached_data[node]['free_disk_space'] -= data['storage']

            node_usage_status[cached_data[node]['topic']]['ram'] += data['ram']
            node_usage_status[cached_data[node]['topic']]['gpu'] += data['gpu']
            node_usage_status[cached_data[node]['topic']]['cpu'] += data['cpu']
            node_usage_status[cached_data[node]['topic']]['storage'] += data['storage']
            Node = node
            break
    if Node is not None:
        cached_status[Node] = cached_data[Node]
    return response

def create_app():
    global db
    
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig())

    mongo_client = MongoClient(app.config['MONGO_URL'])
    db = mongo_client.get_database(app.config['MONGO_DB'])

    @app.route('/node_info', methods = ['GET','POST'])
    def get_node_info():
        '''
        This takes up the data from data server
        It Returns details of node on which container can be deployed
        '''
        data = request.json
        print(data)
        resource_data = data['resources']
        response = {}
        # print(data)
        # print(resource_data)
        storage = 0
        # print(resource_data)
        resource_data['ram'] = float(resource_data['ram'][:-1])
        for s in data['storage']:
            size = s['size'][:-1]
            size = float(size)
            storage += size
        
        resource_data['storage'] = storage
        resource_data['container_name'] = data["env_name"] + '_' + data['_id']
        resource_data['_id'] = data['_id']
        resource_data['cpu'] = float(resource_data['cpu'])
        resource_data['gpu'] = int(resource_data['gpu'])
        print("Data Recieved:")
        print(resource_data)
        response = select_node(resource_data,cached_status)
        print(type(response))

        return jsonify(response)
    
    @app.route('/node/failed', methods = ['GET','POST'])
    def update_node_status():
        '''
        In case a container doesnot successfully deployed on
        node then the used resources is updated via this function
        '''
        data = request.json
        print("Failed Data is:",data)
        node_usage_status[data['topic']]['cpu'] += data['cpu']
        node_usage_status[data['topic']]['gpu'] += data['gpu']
        node_usage_status[data['topic']]['ram'] += data['ram']

        return jsonify({"status" : "updated successfully"})

    
    def initiate(db, config, logger):
        initiate_the_usage(db, config, logger)
        global health_thread
        health_thread = Thread(target=get_health, args=('health',db,config,))
        health_thread.start()

    def inter():
        global killed
        killed = False
        health_thread.join()
    
    initiate(db, app.config, app.logger)
    atexit.register(inter)
    return app



def initiate_the_usage(db, config, logger):
    global node_usage_status
    node_monitor_url = get_service(db, config['SERVICES_COLL'], 'node-monitor')
    node_usage_status = get_response(node_monitor_url, config['NODE_MONTIOR_NA_USAGE_API'],None) # need to add coorect ip
    logger.info(f"got node usage stats: {node_usage_status}")


def register_self(config):
    self_ip_addr = get_local_ip()
    if app.config['DEVELOPMENT'] == False:
        self_ip_addr = ip.get()

    app.logger.info(f"registering service {app.config['NODE_MANAGER']} at ip {self_ip_addr}")

    free_port = next_free_port()

    if free_port is None:
        raise ValueError('could not find a free port')
    
    app.logger.info(f"found free port at {free_port}")
    
    if not register_service(db, app.config['SERVICES_COLL'], 
                            app.config['NODE_MANAGER'], 
                            self_ip_addr, free_port):
        raise Exception('could not register service')

    app.logger.info(f"registering service {app.config['NODE_MANAGER']} at ip {self_ip_addr} and port {free_port}")

    return self_ip_addr, free_port

app = create_app()

if __name__ == '__main__':
    ip, port = register_self(app.config)
    app.run(host=ip, port=port,debug=False)
