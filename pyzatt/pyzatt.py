from pyzatt.zkmodules.packet import PacketMixin
from pyzatt.zkmodules.data_user import DataUserMixin
from pyzatt.zkmodules.data_record import DataRecordMixin
from pyzatt.zkmodules.terminal import TerminalMixin
from pyzatt.zkmodules.access import AccessMixin
from pyzatt.zkmodules.realtime import RealtimeMixin
from pyzatt.zkmodules.other import OtherMixin
from prettytable import PrettyTable
import binascii
import struct

"""
Main library file, defines class ZK session to access a device,
and ZKUser class, used to store user's data.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class ZKUser:
    """
    Class to model user's properties.
    """
    def __init__(self):
        self.user_sn = None         # user's internal index
        self.user_id = ''           # user's id
        self.user_name = ''         # user's name
        self.user_password = ''     # user's password
        self.card_number = 0        # user's RF card number
        self.admin_level = 0        # user's admin level
        self.not_enabled = 1        # user's enable flag(active=0)
        # user's fingerprint templates
        # with the format [fp template, fp flag]
        self.user_fptmps = [[0, 0]]*10
        self.user_group = 1
        self.user_tzs = [1, 0, 0]

    def set_user_info(self, user_sn, user_id, name="",
                      password="", card_no=0,
                      admin_lv=0, neg_enabled=0,
                      user_group=1, user_tzs=[1, 0, 0]):
        """
        Changes the user data fields.

        :param user_sn: Integer, serial number.
        :param user_id: String, user ID.
        :param name: String, user name, must be <=23.
        :param password: String, user password, 8 chars long.
        :param card_no: Integer, user RF card number.
        :param admin_lv: Integer, user admin level.
        :param neg_enabled: Integer, user enable flag,
            (0=enabled, 1=disabled).
        :param user_group: Integer, group number to which the user belongs.
        :param user_tzs: List of integers, timezones of the user, if it is
            an empty array, it should be assumed that the user is using the
            group's timezones.
        :return: None.
        """
        self.user_sn = user_sn
        self.user_id = user_id
        self.user_name = name
        self.user_password = password
        self.card_number = card_no
        self.admin_level = admin_lv
        self.not_enabled = neg_enabled
        self.user_group = user_group
        self.user_tzs = user_tzs

    def get_sn(self):
        """
        Returns the user's internal index on machine.

        :return: Integer.
        """
        return self.user_sn

    def set_user_fptmp(self, fp_index, fp_tmp, fp_flag):
        """
        Stores a fingerprint template in a ZKUser instance.

        :param fp_index: Integer, fingerprint index, valid values [0,9].
        :param fp_tmp: Bytearray, fingerprint template.
        :param fp_flag: Integer, type of fingerprint, valid(1) or duress(3).
        :return: None.
        """
        self.user_fptmps[fp_index] = [fp_tmp, fp_flag]

    def ser_user(self):
        """
        Builds user entry.

        :return: Bytearray, with the users info.
        """
        user_info = bytearray([0x00] * 72)
        user_info[0:2] = struct.pack('<H', self.user_sn)
        user_info[2] = (self.admin_level << 1) | self.not_enabled
        user_info[3:3+len(self.user_password)] = self.user_password.encode()
        user_info[11:11+len(self.user_name)] = self.user_name.encode()
        user_info[35:39] = struct.pack('<I', self.card_number)
        user_info[39] = self.user_group

        if len(self.user_tzs) != 0:
            user_info[40:42] = bytes([1, 0])
            user_info[42:44] = struct.pack('<H', self.user_tzs[0])
            user_info[44:46] = struct.pack('<H', self.user_tzs[1])
            user_info[46:48] = struct.pack('<H', self.user_tzs[2])

        user_info[48:48 + len(self.user_id)] = self.user_id.encode()
        return user_info


class ATTen:
    """
    Attendance log entry.
    """
    def __init__(self, user_sn, user_id, ver_type, att_time, ver_state):
        """
        :param user_sn: Integer, user's index on machine.
        :param user_id: Str, user's ID.
        :param ver_type: Integer, verification type of attendance.
        :param att_time: Datetime object, time of the record.
        :param ver_state: Integer, verification state.
        """
        self.user_sn = user_sn
        self.user_id = user_id
        self.ver_type = ver_type
        self.att_time = att_time
        self.ver_state = ver_state


class OPen:
    """
    Operation log entry.
    """
    def __init__(self, op_id, op_time, param1, param2, param3, param4):
        """
        :param op_id: Integer, operation code.
        :param op_time: Datetime object, time of the record.
        :param param1: Parameter 1.
        :param param2: Parameter 2.
        :param param3: Parameter 3.
        :param param4: Parameter 4.
        """
        self.op_id = op_id
        self.op_time = op_time
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4


class ZKSS(PacketMixin, DataUserMixin,
           DataRecordMixin, TerminalMixin,
           AccessMixin, RealtimeMixin, OtherMixin):

    def __init__(self):
        self.reply_number = 0           # reply counter
        self.session_id = 0             # session id
        self.connected_flg = False      # connection flag
        self.dev_platform = ''          # platform name
        self.firmware_v = ''            # firmware version
        self.users = {}                 # dict of ZKUser, the key is the id
        self.att_log = []               # list of attendance entries
        self.op_log = []                # list of operation entries

    def add_user(self, user_sn):
        """
        Appends an empty user instance, given the user index,
        to the list of users of the current session.

        :param user_sn: Integer, user's index on machine.
        :return: None.
        """
        if user_sn not in self.users:
            self.users[user_sn] = ZKUser()

    def id_exists(self, user_id):
        for sn in self.users:
            if self.users[sn].user_id == user_id:
                return True
        return False

    def create_user(self):
        try:
            new_user_sn = max(list(self.users.keys()))+1
        except ValueError:
            new_user_sn = 1
        self.add_user(new_user_sn)
        return new_user_sn

    def print_users_summary(self, users_sns=None):
        """
        Prints a table with relevant users data and another with the
        templates with the corresponding owners,
        read_all_user_id and read_all_fptmp should be called before, since
        this function only prints the contents of the ZKUser list object.

        :return: None.
        """
        if users_sns is None:
            users_sns = self.users.keys()

        # create users info table
        # fields to show
        t_headers = ['User internal index', 'User ID', 'User name',
                     'Password', 'Card number', 'Admin level', 'Enabled',
                     'Group number', 'Timezones']

        summ_table = PrettyTable(t_headers)

        # adds a row for each user
        for sn in users_sns:
            zuser = self.users[sn]
            summ_table.add_row([
                                sn,
                                zuser.user_id,
                                zuser.user_name,
                                zuser.user_password,
                                zuser.card_number,
                                zuser.admin_level,
                                True if zuser.not_enabled == 0 else False,
                                zuser.user_group,
                                zuser.user_tzs
                                ])
        # show table
        print(summ_table)

        # create fp template table
        # fields to show
        t_headers = ['User ID', 'User name',
                     'Finger index', 'Fingerprint type',
                     'Fingerprint template']

        fptmp_table = PrettyTable(t_headers)

        # adds a row for each template
        for sn in users_sns:

            zuser = self.users[sn]

            for fp_idx in range(len(zuser.user_fptmps)):
                # if fp template doesn't exists, skip
                if not zuser.user_fptmps[fp_idx][0]:
                    continue

                # add template, index and flag to table row
                fptmp = zuser.user_fptmps[fp_idx][0]
                flg = zuser.user_fptmps[fp_idx][1]
                fptmp_table.add_row([
                    zuser.user_id,
                    zuser.user_name,
                    fp_idx,
                    flg,
                    '%s...' % binascii.hexlify(fptmp[:15]).decode('ascii')
                ])

        print(fptmp_table)

    def print_attlog(self):
        """
        Prints a table with attendance log entries, the function read_att_log
        should be called before calling this function.

        :return: None.
        """
        t_headers = ['User internal index', 'User ID', 'Verification type',
                     'Verification state', 'Attendance time']

        att_table = PrettyTable(t_headers)

        for att_entry in self.att_log:
            att_table.add_row([
                att_entry.user_sn,
                att_entry.user_id,
                att_entry.ver_type,
                att_entry.ver_state,
                att_entry.att_time
            ])
        # show table
        print(att_table)

    def print_oplog(self):
        """
        Prints a table with the operation log entries,
        the function read_op_log, should be called before calling this
        function.

        :return: None.
        """
        t_headers = ['Operation ID', 'Operation time', 'Param 1',
                     'Param 2', 'Param 3', 'Param 4']

        op_table = PrettyTable(t_headers)

        for op_entry in self.op_log:
            op_table.add_row([
                op_entry.op_id,
                op_entry.op_time,
                op_entry.param1,
                op_entry.param2,
                op_entry.param3,
                op_entry.param4
            ])
        # show table
        print(op_table)

    def id_to_sn(self, user_id):
        """
        Obtains the user id, given the user internal index.

        :param user_id: Str, user's ID.
        :return: Integer, user's index on machine,
            if the user doesn't exists, returns -1.
        """
        for sn in self.users:
            if self.users[sn].user_id == user_id:
                return sn
        return -1

    def append_att_entry(self, user_sn, user_id, ver_type,
                         att_time, ver_state):
        """
        Appends an attendance log entry to the attendance object.

        :param user_sn: Integer, user's index.
        :param user_id: Str, user's ID.
        :param ver_type: Integer, verification type.
        :param att_time: Datetime, time of the record.
        :param ver_state: Integer, verification state.
        :return: None.
        """
        self.att_log += [ATTen(user_sn, user_id, ver_type,
                               att_time, ver_state)]

    def append_op_entry(self, op_id, op_time, param1,
                        param2, param3, param4):
        """
        Appends an operation log entry to the operation records object.

        :param op_id: Integer, operation code.
        :param op_time: Datetime, time of the record.
        :param param1: Parameter 1.
        :param param2: Parameter 2.
        :param param3: Parameter 3.
        :param param4: Parameter 4.
        :return: None.
        """
        self.op_log += [OPen(op_id, op_time, param1,
                             param2, param3, param4)]
