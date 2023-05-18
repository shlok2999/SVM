from kafka import KafkaProducer
import time
import json
from helper import *

environment_data = get_environment_details()

class Kafka_Producer:
    def __init__(self,topic):
        self.bootstrap_servers = environment_data['bootstrap_servers']
        self.producer = KafkaProducer(bootstrap_servers = self.bootstrap_servers, 
                                    value_serializer=self.serializer)
        self.topic = topic


    def serializer(self, message):
        return json.dumps(message).encode('utf-8')

    def send_valid_config(self, message):
        self.producer.send(self.topic, message)
        time.sleep(1)
