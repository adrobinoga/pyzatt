import struct
from pyzk.zkmodules.defs import *
from pyzk.misc import *

"""
This file contains the functions related to manage records
in attendance devices.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


class DataRecordMixin:

    def read_att_log(self):
        """
        Requests the attendance log.

        :return: None. Stores the attendance log entries
        in the att_log attribute.
        """
        self.send_command(id=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('010d000000000000000000'))
        self.recv_long_reply()

        # clear the attendance log attribute
        self.att_log = []

        # get number of log entries
        att_count = struct.unpack('<H', self.last_payload_data[0:2])[0]/40

        # skip the size of log and zeros
        i = 4

        # extract the fields from each log entry
        for idx in range(att_count):
            # user internal index
            user_sn = struct.unpack('<H', self.last_payload_data[i:i+2])[0]
            # user id
            user_id = self.last_payload_data[i+2:i+11].decode('ascii').\
                replace('\x00', '')
            # verification type
            ver_type = self.last_payload_data[i+26]
            # time of the record
            att_time = decode_time(self.last_payload_data[i+27:i+31])
            # verification state
            ver_state = self.last_payload_data[i+31]

            # append attendance entry
            self.append_att_entry(user_sn, user_id, ver_type, att_time, ver_state)

            idx += 40

    def clear_att_log(self):
        """
        Delete the attendance log record on the machine.

        :return: None.
        """
        self.send_command(id=CMD_CLEAR_ATTLOG)
        self.recv_reply()
        self.refresh_data()

    def read_op_log(self):
        """
        Requests the operation log.

        :return: None. Stores the operation log in the op_log attribute.
        """
        self.send_command(id=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('0122000000000000000000'))
        self.recv_long_reply()

        # clears the operation log attribute
        self.op_log = []

        # extracts number of op log entries
        op_count = struct.unpack('<H', self.last_payload_data[0:2])[0] / 16

        # skips the log size and zeros
        i = 4
        # extracts the operation fields from each entry
        for idx in range(op_count):
            op_id = self.last_payload_data[i+4]
            op_time = decode_time(self.last_payload_data[i + 4:i + 8])
            params = 4*[0]
            for n in range(len(params)):
                params[n] = struct.unpack('<H',
                                          self.last_payload_data[
                                            i + (n*2): i + ((n + 1) * 2)
                                          ])[0]
            # append operation log entry
            self.append_op_entry(op_id, op_time, params[0], params[1], params[2], params[3])

            idx += 16


    def clear_op_log(self):
        """
        Delete the operation record on machine.

        :return: None.
        """
        self.send_command(id=CMD_CLEAR_OPLOG)
        self.recv_reply()
        self.refresh_data()