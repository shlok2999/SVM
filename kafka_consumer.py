import json 
from kafka import KafkaConsumer
from docker_create import *

class Kafka_Consumer:
    def __init__(self):
        self.bootstrap_servers = ['localhost:9092']
        self.auto_offset_reset = 'earliest'
        self.topic = 'demo_svm'
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset=self.auto_offset_reset
        )
if __name__ == '__main__':
    kafka_consumer_obj = Kafka_Consumer()
    file_desc = open('env_install_schema.json', 'r')
    installation_steps = json.load(file_desc)
    file_desc.close()

    for message in kafka_consumer_obj.consumer:
        print(json.loads(message.value))
        json_data = json.loads(message.value)
        init_env_setup_steps(installation_steps, json_data)

