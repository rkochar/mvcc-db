from kafka import KafkaConsumer

import logging

logging.basicConfig(level=logging.INFO)


class ConsumerHelper:

    def __init__(self, topic, group):
        self.kafka_host = "kafka-service.kafka:9092"
        self.consumer = KafkaConsumer(
            topic,
            group_id=group,
            bootstrap_servers=self.kafka_host,
        )
