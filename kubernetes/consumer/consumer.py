from kafka import KafkaConsumer
import time

import logging
logging.basicConfig(level=logging.INFO)

import utils.mvcc as mvcc
import utils.consumer as kafka_consumer


def update_mvcc(mvccdb, messages):
    logging.info(f"Update mvcc {messages}")
    # for message in messages:
    #    mvccdb[message.key].append(message.version, message.value)
    return mvccdb


def process_transaction(mvccdb, transaction):
    logging.info(f"Transaction received: {transaction}")
    return mvccdb


def consume_kafka_messages(mvccdb, transaction_consumer, updates_consumer):
    logging.info("Starting to consume messages")
    while True:
        time.sleep(3)
        messages = updates_consumer.poll(timeout_ms=100)
        if messages != {}:
            mvccdb = update_mvcc(mvccdb, messages)

        time.sleep(3)
        transaction = transaction_consumer.poll(timeout_ms=100, max_records=1)
        if transaction != {}:
            mvccdb = process_transaction(mvccdb, transaction)


if __name__ == "__main__":
    logging.info("Starting consumer")
    mvccdb = mvcc.MVCC(items=12).mvcc
    transaction_consumer = kafka_consumer.ConsumerHelper(topic="topic-transaction", group="group-transaction").consumer
    updates_consumer = kafka_consumer.ConsumerHelper(topic="topic-update", group="group-update").consumer
    consume_kafka_messages(mvccdb, transaction_consumer, updates_consumer)
