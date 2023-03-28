import requests
import json


def get_response(ip_address,data):
    ans = requests.get(ip_address, params=data).content.decode()
    ans = json.loads(ans)
    return ans
    