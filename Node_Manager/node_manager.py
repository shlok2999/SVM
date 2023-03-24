import json
from flask import Flask, jsonify, request
from threading import Thread

cached_status = dict()
app = Flask(__name__)

def get_health(thread_name):
    '''
    Fetch IPs from central DB
    And get health of all new Nodes Available
    '''
    pass

@app.route('/node_info')
def get_node_info():
    data = request.args.to_dict()

if __name__ == '__main__':
    status_thread = Thread( target=get_health, args=("health_status_thread", ) )
    app.run(host="0.0.0.0", port=8080, debug=True)
    status_thread.join()
