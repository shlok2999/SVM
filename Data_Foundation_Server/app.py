import json
from flask import Flask, jsonify
from json_schema_validator import *
from kafka_producer import Kafka_Producer
from helper import *
# from django.http import JsonResponse

app = Flask(__name__)



@app.route("/config")
def get_env_config():
    file_desc = open('dfs_contract.json')
    data = json.load(file_desc)
    file_desc.close()


    if validate_config(data):
        ans = get_response('http://127.0.0.1:8000/search',data['resources'])
        kafka_producer_obj = Kafka_Producer(ans['topic'])
        kafka_producer_obj.send_valid_config(data)
        response = {'response':'config valid'}
        return jsonify(response)

    response = {'response':'config not valid'}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)