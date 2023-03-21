from kafka import KafkaProducer
import time
import json
class Kafka_Producer:
    def __init__(self):
        self.bootstrap_servers = ['localhost:9092']
        self.producer = KafkaProducer(bootstrap_servers = self.bootstrap_servers, 
                                    value_serializer=self.serializer)
        self.topic = "demo_svm"


    def serializer(self, message):
        return json.dumps(message).encode('utf-8')

    def send_valid_config(self, message):
        self.producer.send(self.topic, message)
        time.sleep(1)
