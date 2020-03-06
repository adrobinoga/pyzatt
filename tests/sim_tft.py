#!/usr/bin/python3.5

import socket
"""
Simulates a TFT device, by setting up a TCP server and handling requests
from a test script or another program.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

HOST = 'localhost'
PORT = 4370

class TFT:
    def __init__(self):
        self.firmware_version =
        self.dev_state = 0
        self.pin_width = 9
        self.client_zk = None

        self.zk_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.zk_srv.bind((HOST,PORT))
        self.zk_srv.listen(0)

    def accept_client(self):
        self.client_zk,d = self.zk_srv.accept()

    def parse_packet(self):

