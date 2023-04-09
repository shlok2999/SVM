import json 
from kafka import KafkaConsumer
from docker_create import *
import uuid
from helper import *
from subprocess import Popen, PIPE


environment_data = get_environment_details()

class Kafka_Consumer:
    def __init__(self,topic):
        print(environment_data)
        self.bootstrap_servers = environment_data['bootstrap_servers']
        print(self.bootstrap_servers,type(self.bootstrap_servers))
        self.auto_offset_reset = 'latest'
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset=self.auto_offset_reset
        )
if __name__ == '__main__':
    topic = str(hex(uuid.getnode()))
    # print(topic) 
    kafka_consumer_obj = Kafka_Consumer(topic)
    file_desc = open('env_install_schema.json', 'r')
    installation_steps = json.load(file_desc)
    file_desc.close()

    for message in kafka_consumer_obj.consumer:
        print(json.loads(message.value))
        # print(type(message.value))
        json_data = json.loads(message.value)
        init_env_setup_steps(installation_steps, json_data)

