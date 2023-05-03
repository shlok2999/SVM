import json
from flask import Flask, jsonify, request
from threading import Thread
from helper import *
import time
import atexit

cached_status = dict() # Used to store the current free resources in nodes
killed = True
health_thread = None
node_usage_status = dict() # Used to know how much resource of each node is already used
environment_details = get_environment_details()

def initiate_the_usage():
    global node_usage_status
    node_usage_status = get_response(environment_details['node_monitor'],'/send_usage',None) # need to add coorect ip
    print(node_usage_status)

NODE_AGENT1="http://127.0.0.1:8010"

def get_node_ip():
    return [f'{NODE_AGENT1}/node_status']

def get_health(thread_name):
    '''
    Fetch IPs from central DB
    And get health of all new Nodes Available
    '''
    global cached_status
    global killed
    print('in get health')
    while(killed):
        node_ip = get_node_ip()
        current_status = dict()
        for ip in node_ip:
            topic = None
            try:
                # print('sending request to :',ip)
                response = get_response(ip,"",None)
                # print('got response',response)
                topic = response['topic']
                current_status[response['topic']] = response
                if response['topic'] not in node_usage_status:
                    node_usage_status[response['topic']] = get_response(environment_details['node_monitor'],'/topic_usage',{'topic':response['topic']})
            except:
                if topic is not None:
                    del node_usage_status[topic]
        
        for topic in node_usage_status.keys():
            current_status[topic]['cpu_count'] -= node_usage_status[topic]['cpu']
            current_status[topic]['gpu_count'] -= node_usage_status[topic]['gpu']
            current_status[topic]['free_ram'] -= node_usage_status[topic]['ram']

        cached_status = current_status
        # print(node_usage_status)
        # print(cached_status)
        time.sleep(5)

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
    
    for node in cached_data.keys():
        print(cached_data[node])
        if data['ram'] <= cached_data[node]['free_ram'] and data['cpu'] <= cached_data[node]['cpu_count'] and data['gpu'] <= cached_data[node]['gpu_count'] and data['storage'] <= cached_data[node]['free_disk_space']:
            response['topic'] = cached_data[node]['topic']
            response['resource_available'] = True
            post_data = data
            post_data['topic'] = cached_data[node]['topic']
            print(post_response(environment_details['node_monitor'], "/add_container", post_data))

            cached_data[node]['free_ram'] -= data['ram']
            cached_data[node]['gpu_count'] -= data['gpu']
            cached_data[node]['cpu_count'] -= data['cpu']
            cached_data[node]['free_disk_space'] -= data['storage']

            node_usage_status[cached_data[node]['topic']]['ram'] += data['ram']
            node_usage_status[cached_data[node]['topic']]['gpu'] += data['gpu']
            node_usage_status[cached_data[node]['topic']]['cpu'] += data['cpu']
            node_usage_status[cached_data[node]['topic']]['storage'] += data['storage']
            
            break
    cached_status = cached_data
    return response

def create_app():
    app = Flask(__name__)
    @app.route('/node_info', methods = ['GET','POST'])
    def get_node_info():
        '''
        This takes up the data from data server
        It Returns details of node on which container can be deployed
        '''
        data = request.json
        resource_data = data['resources']
        response = {}
        print(data)
        print(resource_data)
        storage = 0
        # print(resource_data)
        resource_data['ram'] = float(resource_data['ram'][:-1])
        for s in data['storage']:
            size = s['size'][:-1]
            size = float(size)
            storage += size
        
        resource_data['storage'] = storage
        resource_data['container_name'] = data["env_name"]
        resource_data['_id'] = data['_id']
        resource_data['cpu'] = float(resource_data['cpu'])
        resource_data['gpu'] = int(resource_data['gpu'])
        print("Data Recieved:")
        print(resource_data)
        response = select_node(resource_data,cached_status)
        print(type(response))

        return jsonify(response)
    
    @app.route('/node_failed', methods = ['GET','POST'])
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
    
    def initiate():
        initiate_the_usage()
        global health_thread
        health_thread = Thread(target=get_health, args=('health',))
        health_thread.start()

    def inter():
        global killed
        killed = False
        health_thread.join()
    
    initiate()
    atexit.register(inter)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)
