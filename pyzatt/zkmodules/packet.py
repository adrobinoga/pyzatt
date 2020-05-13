import struct
import pyzatt.zkmodules.defs as DEFS
import pyzatt.misc as misc

"""
This file contains provides functions to create, parse, receive and send,
packets, it also suppors reading of large datasets(see ex_data protocol spec).

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class PacketMixin:

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
        zk_packet = bytearray(DEFS.START_TAG)  # fixed tag
        zk_packet.extend([0x00] * 2)  # size of payload
        zk_packet.extend([0x00] * 2)  # fixed zeros
        zk_packet.extend(struct.pack('<H', cmd_code))  # cmd code / reply id
        zk_packet.extend([0x00] * 2)  # checksum field

        # append session id
        if session_id is None:
            zk_packet.extend(struct.pack('<H', self.session_id))
        else:
            zk_packet.extend(struct.pack('<H', session_id))

        # append reply number
        if reply_number is None:
            zk_packet.extend(struct.pack('<H', self.reply_number))
        else:
            zk_packet.extend(struct.pack('<H', reply_number))

        # append additional data
        if data:
            zk_packet.extend(data)

        # write size field
        zk_packet[4:6] = struct.pack('<H', len(zk_packet) - 8)
        # write checksum
        zk_packet[10:12] = struct.pack('<H', misc.checksum16(zk_packet[8:]))

        return zk_packet

    def recv_reply(self, buff_size=1024):
        """
        Receives data from the device.

        :param buff_size: Int, maximum amount of data to receive,
            if not specified, is set to 1024, also updates the reply number,
            and stores fields of the packet to the attributes:

            - self.last_reply_code
            - self.last_session_code
            - self.last_reply_counter
            - self.last_payload_data
        :return: Bytearray, received data,
            also stored in last_payload_data.
        """
        zkp = self.soc_zk.recv(buff_size)
        zkp = bytearray(zkp)
        self.parse_ans(zkp)
        self.reply_number += 1

    def recv_long_reply(self, buff_size=4096):
        """
        Receives a large dataset from the device.

        :param buff_size: Int, maximum amount of data to receive,
            if not specified, is set to 1024.
        :return: Bytearray, received dataset, if the it extract the dataset,
            returns an emtpy bytearray.
        """
        zkp = self.recv_packet(buff_size)
        self.parse_ans(zkp)
        self.reply_number += 1

        dataset = bytearray([])

        if self.last_reply_code == DEFS.CMD_DATA:
            # device sent the dataset immediately, i.e. short dataset
            dataset = self.last_payload_data

        elif self.last_reply_code == DEFS.CMD_PREPARE_DATA:
            # seen on fp template download procedure

            # receives packet with long dataset
            zkp = self.recv_packet()
            self.parse_ans(zkp)
            dataset = self.last_payload_data

            # receives the acknowledge after the dataset packet
            self.recv_packet(buff_size)

        elif self.last_reply_code == DEFS.CMD_ACK_OK:
            # device sent the dataset with additional commands, i.e. longer
            # dataset, see ex_data spec
            size_info = struct.unpack('<I', self.last_payload_data[1:5])[0]

            # creates data for "ready for data" command
            rdy_struct = bytearray(4 * [0])
            rdy_struct.extend(struct.pack('<I', size_info))

            self.send_command(DEFS.CMD_DATA_RDY, data=bytearray(rdy_struct))

            # receives the prepare data reply
            self.recv_packet(24)

            # receives packet with long dataset
            dataset = bytearray()
            while True:
                zkp = self.recv_packet()
                self.parse_ans(zkp)
                if (self.last_reply_code == DEFS.CMD_DATA):
                    dataset += self.last_payload_data
                else:
                    break

            # increment reply number and send "free data" command
            self.reply_number += 1
            self.send_command(DEFS.CMD_FREE_DATA)

            # receive acknowledge
            self.recv_packet(buff_size)

            # update reply counter
            self.reply_number += 1

        return dataset

    def recv_packet(self, buff_size=4096):
        """
        Receives a packet from the device.

        :param buff_size: Int, buffer size used for socket receive.
        :return: Bytearray, received data.
        """
        zkp = self.recv_data(buff_size)
        # extracts size of the total packet
        total_size = 8 + struct.unpack('<H', zkp[4:6])[0]
        rem_recv = total_size - len(zkp)
        # keeps reading until it receives the complete packet
        while len(zkp) < total_size:
            zkp += self.recv_data(rem_recv)
            rem_recv = total_size - len(zkp)
        return zkp

    def recv_data(self, buff_size=4096):
        """
        Receives data from the device.

        :param buff_size: Int, maximum amount of data to receive,
            if not specified, is set to 1024.
        :return: Bytearray, received data.
        """
        return bytearray(self.soc_zk.recv(buff_size))

    def recv_event(self):
        """
        Receives an event from the machine and sends an acknowledge reply.

        :return: None,
            stores the code of the event in the last_event_code variable,
            it also stores the data contents in the last_payload_data variable.
        """
        self.parse_ans(self.recv_packet())
        self.last_event_code = self.last_session_code
        self.send_packet(self.create_packet(DEFS.CMD_ACK_OK, reply_number=0))

    def get_last_packet(self):
        """
        Returns the last received packet.

        :return: Bytearray, a whole packet.
        """
        return self.last_packet

    def send_command(self, cmd, data=None):
        """
        Sends a packet with a given command, payload data field
        may be also included.

        :param cmd: Integer, command id.
        :param data: Bytearray, data to be placed in the data field
            of the payload.
        :return: None.
        """
        self.send_packet(self.create_packet(cmd, data))

    def send_packet(self, zkp):
        """
        Sends a given complete packet.

        :param zkp: Bytearray, packet to send.
        :return: None.
        """
        self.soc_zk.send(zkp)

    def parse_ans(self, zkp):
        """
        Checks fixed fields of a given packet and extracts the reply code,
        session code, reply counter and data of payload, to the attributes:

        - self.last_reply_code
        - self.last_session_code
        - self.last_reply_counter
        - self.last_payload_data

        :param zkp: Bytearray, packet.
        :return: Bool, returns True if the packet is valid, False otherwise.
        """
        self.last_reply_code = -1
        self.last_session_code = -1
        self.last_reply_counter = -1
        self.last_payload_data = bytearray([])

        # check the start tag
        if not zkp[0:4] == DEFS.START_TAG:
            print("Bad start tag")
            return False

        # extracts size of packet
        self.last_reply_size = struct.unpack('<I', zkp[4:8])[0]

        # checks the checksum field
        if not misc.is_valid_payload(zkp[8:]):
            print("Invalid checksum")
            return False

        # stores the packet fields to the listed attributes

        self.last_packet = zkp

        self.last_reply_code = struct.unpack('<H', zkp[8:10])[0]

        self.last_session_code = struct.unpack('<H', zkp[12:14])[0]

        self.last_reply_counter = struct.unpack('<H', zkp[14:16])[0]

        self.last_payload_data = zkp[16:]

    def recvd_ack(self):
        """
        Checks if the last reply returned an acknowledge packet.

        :return: Bool, True if the last reply was an CMD_ACK_OK reply,
            returns False if otherwise.
        """
        if self.last_reply_code == DEFS.CMD_ACK_OK:
            return True
        else:
            return False
