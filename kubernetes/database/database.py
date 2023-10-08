from utils.consumer import ConsumerHelper, parse_kafka_message
from utils.producer import ProducerHelper
from time import sleep

import utils.mvcc as mvcc

import logging
logging.basicConfig(level=logging.INFO)

def process_write(mvccdb, transaction, update_producer):
    logging.info(f"Writing transaction {transaction}")
    logging.info(f"MVCCDB: {mvccdb}")
    old_value_sender, old_value_receiver = mvccdb[transaction["sender"]][-1], mvccdb[transaction["receiver"]][-1]
    logging.info(f"Old value sender: {old_value_sender}, new_value_receiver: {old_value_receiver}")
    if old_value_sender[1] >= transaction["amount"]:
        mvccdb[transaction["sender"]].append((old_value_sender[0] + 1, old_value_sender[1] - transaction["amount"]))
        mvccdb[transaction["receiver"]].append((old_value_receiver[0] + 1, old_value_receiver[1] + transaction["amount"]))
        transaction["latest_version_sender"] = mvccdb[transaction["sender"]][-1]
        transaction["latest_version_receiver"] = mvccdb[transaction["receiver"]][-1]
        update_producer.publish_to_kafka(transaction)
        logging.info(f"Transaction {transaction} written")
    else:
        logging.info(f"Transaction rejected: {transaction}")
    return mvccdb

def consume_wites(mvccdb, write_consumer, update_producer):
    logging.info("Database is consuming writes")
    while True:
        write = write_consumer.poll(timeout_ms=1000, max_records=1)
        if write != {}:
            logging.info(f"Database received write: {write}")
            mvccdb = process_write(mvccdb, parse_kafka_message(write)[0], update_producer)
        else:
            sleep(1)

if __name__ == "__main__":
    logging.info("Starting database")
    mvccdb = mvcc.MVCC(items=12).mvcc
    write_consumer = ConsumerHelper(topic="topic-write", group="group-write").consumer
    update_producer = ProducerHelper(topic="topic-update")
    consume_wites(mvccdb, write_consumer, update_producer)
