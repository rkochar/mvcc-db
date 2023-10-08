import json
import logging

import faker
from kafka import KafkaProducer
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO)

class ProducerHelper:

    ACCOUNTS = 12

    def __init__(self, topic):
        self.kafka_topic = topic
        self.kafka_host = "kafka-service.kafka:9092"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_host,
            value_serializer=lambda v: json.dumps(v).encode(),

        )

    def publish_to_kafka(self, message):
        try:
            self.producer.send(self.kafka_topic, message)
            self.producer.flush()
        except KafkaError as ex:
            logging.error(f"Exception {ex}")
        else:
            logging.info(f"{self.kafka_topic}: Published message: {message}")

    @staticmethod
    def create_random_transaction():
        f = faker.Faker()

        new_contact = dict(
            sender=str(f.random_int(min=0, max=ProducerHelper.ACCOUNTS - 1)),
            receiver=str(f.random_int(min=0, max=ProducerHelper.ACCOUNTS - 1)),
            amount=f.random_int(min=1, max=10),
        )
        if new_contact["sender"] == new_contact["receiver"]:
            new_contact["sender"] = str((int(new_contact["sender"]) + 1) % ProducerHelper.ACCOUNTS)

        return new_contact


