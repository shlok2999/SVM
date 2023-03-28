import requests
import json


def get_response(ip_address,data):
    # print(data)
    ans = requests.get(ip_address, params=data).content.decode()
    # print(ans)
    ans = json.loads(ans)
    return ans
    