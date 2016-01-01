#!/usr/bin/env python3

import socket
import re
from uuid import getnode as get_mac
from datetime import datetime

from nmap import PortScanner
from requests.exceptions import HTTPError
from m2x.client import M2XClient
import netifaces

def get_ip():
    '''
    Find the local IP to be scanned. Utilize netifaces to be platform independent.
    '''
    gws = netifaces.gateways()
    addresses = netifaces.ifaddresses(gws['default'][netifaces.AF_INET][1])
    return addresses[netifaces.AF_INET][0]['addr']


class Scanner(object):
    '''
    Simplified nmap scanning and retrieval of MAC addresses
    '''
    def __init__(self, ip=get_ip()):
        self.ip = ip
        self.nmap = PortScanner()
        self.scanned = False
        self.unknown = 0
        self.known = 0
        self.total = 0
        self.previous_total = 0
        self.macs = None

    def scan(self):
        self.previous_total = self.total
        self.simple_scan()
        self.scanned = True
        self.total = self._connections()
        self.macs = self._macs()
        self.known = len(self.macs)
        self.unknown = self.total - self.known

    def simple_scan(self):
        self.nmap.scan(hosts=self.ip+'/24', arguments='-n -sP -PE -PA21,23,80,3389')

    def _macs(self):
        if not self.scanned:
            self.simple_scan()

        macs = {host: self.nmap[host]['addresses'].get('mac', None) for host in self.nmap.all_hosts()}
        
        #nmap often doesn't produce current device MAC address
        if not macs[self.ip]:
            macs[self.ip] = ":".join(re.findall('..', '%012x' % get_mac())).upper()

        # After checking the local device IP, any more connections missing MACS are unknown
        known_macs = [value for value in macs.values() if value]
        return known_macs

    def _connections(self):
        try:
            return int(self.nmap.scanstats()['uphosts'])
        except AssertionError:
            self.simple_scan()
            return int(self.nmap.scanstats()['uphosts'])


    def get_macs_string(self):
        if self.scanned:
            return ", ".join(self.macs)
        self.scan()
        return ", ".join(self.macs)


class Controller(object):
    '''
    Class for interacting with m2x device with known stream names
    '''
    def __init__(self, client, devicename, non_numeric_name, *numeric_names):
        self.client = client
        self.device = self._get_device(devicename)
        self.mac_addresses = self._get_stream(non_numeric_name, numeric=False)
        self.num_macs, self.num_connects, self.num_unknowns = self._get_streams(*numeric_names)

    def update_all(self, scanner):
        # Perform the scan
        scanner.scan()

        # If the number of connections changes, update the stream.
        if scanner.previous_total != scanner.total:
            print('Updating stream')
            posttime = datetime.now()

            values = {self.mac_addresses.name: [{'timestamp': posttime, 'value': scanner.get_macs_string()}],
                      self.num_macs.name: [{'timestamp': posttime, 'value': scanner.known}],
                      self.num_unknowns.name: [{'timestamp': posttime, 'value': scanner.unknown}],
                      self.num_connects.name: [{'timestamp': posttime, 'value': scanner.total}]
                      }

            self.device.post_updates(values=values)
            print('Scan and update complete')
        else:
            print('Stream update not required')

    def _get_device(self, devicename):
        try:
            device = [d for d in self.client.devices(q=devicename) if d.name == devicename][0]
        except IndexError:
            device = self.client.create_device(name=devicename,
                                      description="Local Network Monitor",
                                      visibility="private")
        return device

    def _get_stream(self, name, numeric=True):
        try:
            stream = self.device.stream(name)
        except HTTPError:
            if numeric:
                stream = self.device.create_stream(name)
            else:
                stream = self.device.create_stream(name, type='alphanumeric')
        return stream

    def _get_streams(self, *names, **kwargs):
        streams = []
        numeric = kwargs.get('numeric', True)
        # Get the stream if it exists, if not create the stream.
        for name in names:
            streams.append(self._get_stream(name, numeric))
        return streams
