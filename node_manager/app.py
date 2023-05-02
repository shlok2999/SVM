import json
from flask import Flask, jsonify, request
from threading import Thread
from helper import *
import time
import atexit

cached_status = dict()
killed = True
health_thread = None
node_usage_status = dict()
environment_details = get_environment_details()

def initiate_the_usage():
    global node_usage_status
    node_usage_status = get_response(environment_details['resource_manager'],None) # need to add coorect ip

NODE_AGENT1="http://192.168.42.97:8010"
def create_app():
    app = Flask(__name__)
    @app.route('/node_info')
    def get_node_info():
        data = request.args.to_dict()
        response = select_node(data,cached_status)
        # print(type(response))
        return jsonify(response)
    
    @app.route('/node_failed')
    def update_node_status():
        data = request.args.to_dict()
        node_usage_status[data['topic']]['cpu_count'] += data['cpu']
        node_usage_status[data['topic']]['gpu_count'] += data['gpu']
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
            try:
                print('sending request to :',ip)
                response = get_response(ip,None)
                print('got response',response)
                current_status[response['topic']] = response
                if response['topic'] not in node_usage_status:
                    node_usage_status[response['topic']] = get_response(environment_details['resource_manager'],None)
            except:
                del node_usage_status[response['topic']]
        
        for topic in node_usage_status.keys():
            current_status[topic]['cpu_count'] -= node_usage_status[topic]['cpu_count']
            current_status[topic]['gpu_count'] -= node_usage_status[topic]['gpu_count']
            current_status[topic]['free_ram'] -= node_usage_status[topic]['ram']

        cached_status = current_status
        time.sleep(5)

def select_node(data,cached_data):
    # print(cached_data)
    # return cached_data[list(cached_data.keys())[0]]
    response = {}
    response['resource_available'] = False
    response['topic'] = None
    
    for node in cached_data.keys():
        if data['ram'] <= cached_data[node]['free_ram'] and data['cpu'] <= cached_data[node]['cpu_count'] and data['gpu'] <= cached_data[node]['gpu_count'] and data['storage'] <= cached_data[node]['free_disk_space']:
            response['topic'] = cached_data[node]['topic']
            response['resource_available'] = True
            post_data = data
            post_data['topic'] = cached_data[node]['topic']
            print(post_response(environment_details['resource_manager'], "", post_data))
            break
    return response

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    @app.route('/node_info')
    def get_node_info():
        data = request.args.to_dict()
        response = select_node(data,cached_status)
        # print(type(response))
        return jsonify(response)
    
    def initiate():
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
    app.run(host="192.168.42.24", port=8080,debug=True)
