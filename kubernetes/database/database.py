from utils.consumer import ConsumerHelper
from utils.producer import ProducerHelper
import utils.mvcc as mvcc

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting database")
