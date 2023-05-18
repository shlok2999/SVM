import requests
import json
import socket

def get_response(ip_address,data):
    ans = requests.get(ip_address, params=data).content.decode()
    ans = json.loads(ans)
    return ans

def get_response(ip_address,function,data):
    final_url = f'{ip_address}{function}'
    # print(final_url)
    ans = requests.get(final_url, params=data).content.decode()
    ans = json.loads(ans)
    return ans

def post_response(ip_address,function,data):
    ans = requests.post(ip_address + function, json=data).text
    # ans = json.loads(ans)
    return ans
    
def get_environment_details():
    file_desc = open('environment.json')
    data = json.load(file_desc)
    file_desc.close()
    return data

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        self_ip = s.getsockname()[0]
    except Exception:
        self_ip = '127.0.0.1'
    finally:
        s.close()

    print(self_ip)
    return self_ip

def next_free_port():
    port = 8000
    max_port = 65536
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    return None
