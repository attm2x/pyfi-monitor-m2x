#!/usr/bin/env python3

import os
import time

from m2x.client import M2XClient
from methods import Scanner, Controller

with open('keys.txt', 'r') as f:
    APIKEY = f.readline()

DEVICE_NAME = 'rpi-network-monitor'

CLIENT = M2XClient(key=APIKEY)

# M2X has both numeric and non-numeric streams 
# In this case the mac addresses will be stored as a string
non_numeric_stream = 'mac_addresses'

numeric_streams = ['number_mac_addresses',
                 'total_connections',
                 'number_unknown_connections']

scanner = Scanner()


controller = Controller(CLIENT, DEVICE_NAME, non_numeric_stream, *numeric_streams)

while True:
    print('Beginning scan and stream update')
    controller.update_all(scanner)
    print('Finished scan and update... waiting 1 minute')
    time.sleep(60)
