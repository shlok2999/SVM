import requests
import json


def get_response(ip_address,data):
    ans = requests.get(ip_address, params=data).content.decode()
    ans = json.loads(ans)
    return ans
    
def get_environment_details():
    file_desc = open('environment.json')
    data = json.load(file_desc)
    file_desc.close()
    return data