from pyzk.zkmodules.packet import PacketMixin
from pyzk.zkmodules.data_user import DataUserMixin
from pyzk.zkmodules.data_record import DataRecordMixin
from pyzk.zkmodules.terminal import TerminalMixin
from pyzk.zkmodules.access import AccessMixin
from pyzk.zkmodules.realtime import RealtimeMixin
from pyzk.zkmodules.other import OtherMixin
from prettytable import PrettyTable
from pyzk.misc import *
import binascii

"""
Main library file, defines class ZK session to access a device,
and ZKUser class, used to store user's data.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


class ZKUser:
    def __init__(self):
        self.user_sn = None         # user's internal index
        self.user_id = ''           # user's id
        self.user_name = ''         # user's name
        self.user_password = ''     # user's password
        self.card_number = None     # user's RF card number
        self.admin_level = 0        # user's admin level
        self.not_enabled = 1        # user's enable flag(active=0)
        self.user_fptmps = [[0,0]]*10   # user's fingerprint templates

    def set_user_info(self, user_sn, user_id, name, password,
                      card_no, admin_lv, neg_enabled):
        """
        Changes the user data fields.

        :param user_sn: Integer, serial number.
        :param user_id: String, user ID.
        :param name: String, user name, must be <=23.
        :param password: String, user password, 8 chars long.
        :param card_no: Integer, user RF card number.
        :param admin_lv: Integer, user admin level.
        :param neg_enabled: Integer, user enable flag, valid values {0,1}.
        :return:None.
        """
        self.user_sn = user_sn
        self.user_id = user_id
        self.user_name = name
        self.user_password = password
        self.card_number = card_no
        self.admin_level = admin_lv
        self.not_enabled = neg_enabled

    def set_user_fptmp(self, fp_index, fp_tmp, fp_flag):
        """
        Stores a fingerprint template in a ZKUser instance.

        :param fp_index: Integer, fingerprint index, valid values [0,9].
        :param fp_tmp: Bytearray, fingerprint template.
        :param fp_flag: Integer, type of fingerprint, valid(1) or duress(3).
        :return: None.
        """
        self.user_fptmps[fp_index] = [fp_tmp, fp_flag]


class ZKSS(PacketMixin, DataUserMixin,
           DataRecordMixin, TerminalMixin,
           AccessMixin, RealtimeMixin, OtherMixin):

    def __init__(self):
        self.reply_number = 0
        self.session_id = 0
        self.connected_flg = False
        self.dev_platform = ''
        self.firmware_v = ''
        self.users = {}

    def add_user(self, user_id):
        """
        Appends an empty user instance, given the user id,
        to the list of users of the current session.

        :param user_id: String, user ID.
        :return: None.
        """
        self.users[user_id] = ZKUser()

    def print_users_summary(self):
        """
        Prints a tables with relevant users data,
        read_all_user_id and read_all_fptmp should be called before, since
        this function only prints the contents of the users list object.

        :return: None.
        """
        # create users info table
        # fields to show
        t_headers = ['User internal index', 'User ID', 'User name',
                     'Password', 'Card number', 'Admin level', 'Enabled']

        summ_table = PrettyTable(t_headers)

        # adds a row for each user
        for uid in self.users:
            zuser = self.users[uid]
            summ_table.add_row([
                                str(zuser.user_sn),
                                uid,
                                zuser.user_name,
                                zuser.user_password,
                                zuser.card_number,
                                zuser.admin_level,
                                True if zuser.not_enabled == 0 else False
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
        for uid in self.users:
            zuser = self.users[uid]

            for fp_idx in range(len(zuser.user_fptmps)):
                # if fp template doesn't exists, skip
                if not zuser.user_fptmps[fp_idx][0]:
                    continue

                # add template, index and flag to table row
                fptmp = zuser.user_fptmps[fp_idx][0]
                flg = zuser.user_fptmps[fp_idx][1]
                fptmp_table.add_row([
                    uid,
                    zuser.user_name,
                    fp_idx,
                    flg,
                    '%s...' % binascii.hexlify(fptmp[:15]).decode('ascii')
                ])

        print(fptmp_table)

    def sn_to_id(self, sn):
        """
        Obtains the user id, given the user internal index.

        :param sn: Integer, user's internal index on machine.
        :return: String, user ID, if the user doesn't exists, returns an
        empty string.
        """
        for uid in list(self.users):
            if self.users[uid].user_sn == sn:
                return uid
        return ''
