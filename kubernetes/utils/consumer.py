from kafka import KafkaConsumer
from ast import literal_eval

import logging

logging.basicConfig(level=logging.INFO)


def parse_kafka_message(transaction):
    for _, value in transaction.items():
        return [literal_eval(v.value.decode('utf-8')) for v in value]


class ConsumerHelper:

    def __init__(self, topic, group):
        self.kafka_host = "kafka-service.kafka:9092"
        self.consumer = KafkaConsumer(
            topic,
            group_id=group,
            bootstrap_servers=self.kafka_host,
        )

