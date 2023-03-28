import json 
from kafka import KafkaConsumer
# from docker_create import *
# import uuid

class Kafka_Consumer:
    def __init__(self,topic):
        self.bootstrap_servers = ['localhost:9092']
        self.auto_offset_reset = 'earliest'
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset=self.auto_offset_reset
        )

# if __name__ == '__main__':
#     topic = 'Node_Manger'
#     kafka_consumer_obj = Kafka_Consumer(topic)

#     for message in kafka_consumer_obj.consumer:
#         print(json.loads(message.value))

