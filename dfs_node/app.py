import json
from flask import Flask, jsonify, request
import psutil
import subprocess as sp
import shutil
import uuid

app = Flask(__name__)

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
    # free_gpu_memory = get_gpu_memory() #In MB
    free_gpu_memory = []
    gpu_count = len(free_gpu_memory)
    free_ram = psutil.virtual_memory()[1] #In Bytes
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
    app.run(host="0.0.0.0", port=8090, debug=True)