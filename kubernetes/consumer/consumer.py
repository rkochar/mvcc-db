from ast import literal_eval
import time

import logging
logging.basicConfig(level=logging.INFO)

from utils.mvcc import MVCC
from utils.consumer import ConsumerHelper, parse_kafka_message
from utils.producer import ProducerHelper

def update_mvcc(mvccdb, messages):
    transactions = parse_kafka_message(messages)
    logging.info(f"Transactions accepted: {transactions} for MVCCDB: {mvccdb}")
    for transaction in transactions:
        mvccdb[transaction["sender"]].append(transaction["latest_version_sender"])
        mvccdb[transaction["receiver"]].append(transaction["latest_version_receiver"])
        logging.info(f"Transaction {transaction} written")
    logging.info(f"Finised writing: {transaction} to MVCCDB: {mvccdb}")
    return mvccdb


def process_transaction(mvccdb, transaction, write_producer):
    logging.info(f"Transaction received: {transaction}")
    logging.info(f"MVCCDB: {mvccdb}")
    for t in transaction:
        logging.info(f"sender: {mvccdb[t['sender']][-1]}, amount: {t['amount']}")
        if mvccdb[t["sender"]][-1][1] >= t["amount"]:
            write_producer.publish_to_kafka(t)
        else:
            logging.info(f"Transaction rejected: {t}")


def consume_kafka_messages(mvccdb, transaction_consumer, update_consumer, write_producer):
    logging.info("Starting to consume messages")
    while True:
        time.sleep(3)
        messages = update_consumer.poll(timeout_ms=100)
        if messages != {}:
            mvccdb = update_mvcc(mvccdb, messages)
        transaction = transaction_consumer.poll(timeout_ms=1000, max_records=1)
        if transaction != {}:
            process_transaction(mvccdb, parse_kafka_message(transaction), write_producer)


if __name__ == "__main__":
    logging.info("Starting consumer")
    mvccdb = MVCC(items=12).mvcc
    transaction_consumer = ConsumerHelper(topic="topic-transaction", group="group-transaction").consumer
    update_consumer = ConsumerHelper(topic="topic-update", group="group-update").consumer
    write_producer = ProducerHelper(topic="topic-write")
    consume_kafka_messages(mvccdb, transaction_consumer, update_consumer, write_producer)
