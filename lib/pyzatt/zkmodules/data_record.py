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
        self.send_command(cmd=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('010d000000000000000000'))
        self.recv_long_reply()

        # clear the attendance log attribute
        self.att_log = []

        # get number of log entries
        att_count = struct.unpack('<H', self.last_payload_data[0:2])[0]/40
        att_count = int(att_count)

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

            i += 40

    def clear_att_log(self):
        """
        Delete the attendance log record on the machine.

        :return: None.
        """
        self.send_command(cmd=CMD_CLEAR_ATTLOG)
        self.recv_reply()
        self.refresh_data()

    def read_op_log(self):
        """
        Requests the operation log.

        :return: None. Stores the operation log in the op_log attribute.
        """
        self.send_command(cmd=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('0122000000000000000000'))
        self.recv_long_reply()

        # clears the operation log attribute
        self.op_log = []

        # extracts number of op log entries
        op_count = struct.unpack('<H', self.last_payload_data[0:2])[0] / 16
        op_count = int(op_count)

        # skips the log size and zeros
        i = 4
        # extracts the operation fields from each entry
        for idx in range(op_count):
            op_id = self.last_payload_data[i+2]
            op_time = decode_time(self.last_payload_data[i + 4:i + 8])

            # extract params
            param1 = struct.unpack('<H', self.last_payload_data[i+8:i+10])[0]
            param2 = struct.unpack('<H', self.last_payload_data[i+10:i+12])[0]
            param3 = struct.unpack('<H', self.last_payload_data[i+12:i+14])[0]
            param4 = struct.unpack('<H', self.last_payload_data[i+14:i+16])[0]

            # append operation log entry
            self.append_op_entry(op_id, op_time, param1, param2, param3, param4)

            i += 16


    def clear_op_log(self):
        """
        Delete the operation record on machine.

        :return: None.
        """
        self.send_command(cmd=CMD_CLEAR_OPLOG)
        self.recv_reply()
        self.refresh_data()

    def clear_data(self, data_type=None):
        """
        Deletes types of data.

        :param data_type: Integer, selects the data to be
        deleted on the machine. According to the next list:

        1. Attendance records.
        2. Fingerprint templates.
        4. Operation logs.
        5. User info.

        :return: None.
        """
        if data_type:
            self.send_command(cmd=CMD_CLEAR_DATA, data=bytearray(data_type))
        else:
            self.send_command(cmd=CMD_CLEAR_DATA)
        self.recv_reply()
        self.refresh_data()
