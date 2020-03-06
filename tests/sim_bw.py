#!/usr/bin/python3.5

import socket
import struct
from pyzatt.zkmodules.defs import *
from pyzatt.misc import *

"""
Simulates a Black&White device, by setting up an UDP server
and handling requests from a test script or another program.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

# server address
HOST = 'localhost'
PORT = 4370

params = {
    'firmware_version': 'a.b.c ver Jan 2000'
}
class BW_TERM:
    def __init__(self):
        self.dev_state = 0
        self.pin_width = 9
        self.session_id = 0xf1f2
        self.client = None
        self.zkp = bytearray([])

        # creates socket and binds to pre-defined address
        self.zk_srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.zk_srv.bind((HOST,PORT))

    def create_packet(self, cmd_code, data=None, session_id=None,
                      reply_number=None):
        """
        Creates a packet, given the code and the other optional fields.

        :param cmd_code: Int, Command/reply identifier(see defs.py).
        :param data: Bytearray, data to be placed in the data field
        of the payload.
        :param session_id: Int, session id, if not specified, uses
        the session from connection setup.
        :param reply_number: Int, reply counter, if not specified,
        the reply number is obtained from context.
        :return:
        """
        zk_packet = bytearray()

        zk_packet.extend(struct.pack('<H', cmd_code))  # cmd code / reply id
        zk_packet.extend([0x00] * 2)  # checksum field

        # append session id
        if session_id is None:
            zk_packet.extend(struct.pack('<H', self.session_id))
        else:
            zk_packet.extend(struct.pack('<H', session_id))

        # append reply number
        if reply_number is None:
            zk_packet.extend(struct.pack('<H', self.last_reply_counter))
        else:
            zk_packet.extend(struct.pack('<H', reply_number))

        # append additional data
        if data:
            zk_packet.extend(data)

        # write checksum
        zk_packet[2:4] = struct.pack('<H', checksum16(zk_packet))

        return zk_packet

    def accept_blocking(self):
        # 65k should be enough for simulation purposes
        (zkp, self.client) = self.zk_srv.recvfrom(2**16)
        zkp = bytearray(zkp)
        self.parse_packet(zkp)

    def parse_packet(self, zkp):
        self.last_cmd_code = -1
        self.last_session_code = -1
        self.last_reply_counter = -1
        self.last_payload_data = bytearray([])

        # size of packet
        self.last_reply_size = len(zkp)

        # checks the checksum field
        if not is_valid_payload(zkp):
            print("Invalid checksum")
            return False

        # stores the packet fields to the listed attributes

        self.last_packet = zkp

        self.last_cmd_code = struct.unpack('<H', zkp[0:2])[0]

        self.last_session_code = struct.unpack('<H', zkp[4:6])[0]

        self.last_reply_counter = struct.unpack('<H', zkp[6:8])[0]

        self.last_payload_data = zkp[8:]

        return True

    def process_command(self):

        if self.last_cmd_code == CMD_CONNECT:
            self.zk_srv.sendto(self.create_packet(cmd_code=CMD_ACK_OK),
                               self.client)

        elif self.last_cmd_code == CMD_OPTIONS_WRQ:
            print("Writing param:", self.last_payload_data)
            self.zk_srv.sendto(self.create_packet(cmd_code=CMD_ACK_OK),
                               self.client)


        else:
            print("Unknown command for simulator")
            print_hexdump(self.last_packet)
            self.zk_srv.sendto(self.create_packet(cmd_code=CMD_ACK_UNKNOWN),
                               self.client)


bw_server = BW_TERM()

while True:
    bw_server.accept_blocking()
    bw_server.process_command()