import time
import logging

import utils.producer as kafka_producer


if __name__ == "__main__":
    logging.info("Starting producer")
    transaction_producer = kafka_producer.ProducerHelper(topic="topic-transaction")
    while True:
        time.sleep(1)
        transaction_producer.publish_to_kafka(transaction_producer.create_random_transaction())
