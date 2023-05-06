import json 
from kafka import KafkaConsumer
from docker_create import *
import uuid
from helper import *
from subprocess import Popen, PIPE
from pymongo import MongoClient
from database_ops import *

MONGO_URL = "mongodb+srv://dfs-user:dfssvm2023@dfs-cluster0.qbwo159.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "dfs_db"
SERVICES_COLL = "services"
KAFKA_SERVICE = "kafka"
LIBRARY_COLL = "library"
SERVICES_COLL = "services"

mongo_client = MongoClient(MONGO_URL)
db = mongo_client.get_database(MONGO_DB)


class Kafka_Consumer:
    def __init__(self,topic):
        self.bootstrap_servers = get_kafka_service(db, SERVICES_COLL, KAFKA_SERVICE)
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
    installation_steps = get_installation_steps(db, LIBRARY_COLL)

    for message in kafka_consumer_obj.consumer:
        print(json.loads(message.value))
        # print(type(message.value))
        json_data = json.loads(message.value)
        os_name = json_data["os"]
        init_env_setup_steps(db, SERVICES_COLL, installation_steps[os_name], json_data)

