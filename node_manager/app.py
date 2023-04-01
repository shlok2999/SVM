import json
from flask import Flask, jsonify, request
from threading import Thread
from helper import *
import time
import atexit

cached_status = dict()
killed = True
health_thread = None

def create_app():
    app = Flask(__name__)
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

def get_node_ip():
    return ['http://127.0.0.1:8090/node_status']

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
            print('sending request to :',ip)
            response = get_response(ip,None)
            print('got response',response)
            current_status[ip] = response
        cached_status = current_status
        time.sleep(5)

def select_node(data,cached_data):
    print(cached_data)
    return cached_data[list(cached_data.keys())[0]]



if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8080,debug=True)
