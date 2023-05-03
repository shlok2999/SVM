import json
from flask import Flask, jsonify, request
import psutil
import subprocess as sp
import shutil
import uuid
from config import DevelopmentConfig
from pymongo import MongoClient
from database_ops import *
import bson.json_util as json_util
import logging
import public_ip as ip
from helper import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

mongo_client = MongoClient(app.config['MONGO_URL'])
db = mongo_client.get_database(app.config['MONGO_DB'])
mongo_client = MongoClient(app.config['MONGO_URL'])
db = mongo_client.get_database(app.config['MONGO_DB'])

def register_self():
    self_ip_addr = get_local_ip()
    if app.config['DEVELOPMENT'] == False:
        self_ip_addr = ip.get()

    app.logger.info(f"registering service {app.config['DFS_NODE']} at ip {self_ip_addr}")

    free_port = next_free_port()

    if free_port is None:
        raise ValueError('could not find a free port')
    
    app.logger.info(f"found free port at {free_port}")
    
    service_name = f'{app.config["DFS_NODE"]}_{self_ip_addr}'
    if not register_service(db, app.config['SERVICES_COLL'], 
                            service_name, 
                            self_ip_addr, free_port):
        raise Exception('could not register service')

    app.logger.info(f"registering service {app.config['DFS_NODE']} at ip {self_ip_addr} and port {free_port}")

    return self_ip_addr, free_port

def get_gpu_memory():
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = sp.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
    memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
    return memory_free_values

@app.route('/node_status')
def get_node_status():
    cpu_usage = psutil.cpu_percent(interval = 2)
    cpu_usage_per_proccesor = psutil.cpu_percent(interval = 2,percpu= True)
    cpu_count = len(cpu_usage_per_proccesor)
    free_gpu_memory = get_gpu_memory() #In MB
    # free_gpu_memory = []
    gpu_count = len(free_gpu_memory)
    free_ram = psutil.virtual_memory()[1]/1e9 #Divided by 1e9 to convert Bytes into GB.
    path = '/'
    stat = shutil.disk_usage(path)
    free_disk_space = stat.free/1e9 #Divivded by 1e9 to covert Bytes into GB
    response = {'overall_cpu_usage':cpu_usage,
                'cpu_usage_per_process':cpu_usage_per_proccesor,
                'cpu_count':cpu_count,
                'free_gpu_memory':free_gpu_memory,
                'gpu_count':gpu_count,
                'free_ram':free_ram,
                'free_disk_space':free_disk_space,
                'topic': str(hex(uuid.getnode()))}
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    ip, port = register_self()
    app.run(host=ip, port=port, debug=False)