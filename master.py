#!/usr/bin/env python3

import os
import sys
import time
import logging
import logging.config
import json

from m2x.client import M2XClient
from methods import Scanner, Controller


def setup_logging(default_path='logging.conf',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# Load logging configuration
setup_logging()

logger = logging.getLogger('pyfi')

# Get M2X Master API Key from keys.txt
with open('keys.txt', 'r') as f:
    APIKEY = f.readline().strip()

DEVICE_NAME = 'rpi-network-monitor'

CLIENT = M2XClient(key=APIKEY)

# M2X has both numeric and non-numeric streams
# In this case the mac addresses will be stored as json
non_numeric_stream = 'mac_addresses'

numeric_streams = ['number_mac_addresses',
                   'total_connections',
                   'number_unknown_connections']

scanner = Scanner()


controller = Controller(CLIENT, DEVICE_NAME,
                        non_numeric_stream, *numeric_streams)

if __name__ == "__main__":
    try:
        while True:
            logger.info('Beginning scan')
            controller.update_all(scanner)
            logger.info('Finished... waiting 1 second')
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping network monitor.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception:
        logger.exception("Fatal error in main loop")
