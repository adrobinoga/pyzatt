from pyzk.zkmodules.defs import *
from pyzk.misc import *

"""
This file contains the functions to manage the user's data, fingerprints,
user IDs, passwords, etc.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


class DataUserMixin:
    def read_all_user_id(self):
        """
        Requests all the users info, except the fingerprint templates.

        :return: None.
        """
        self.send_command(CMD_DATA_WRRQ, data=bytearray.fromhex('0109000500000000000000'))
        print_h(self.recv_long_reply())

    def read_all_fptmp(self):
        """
        Requests all the fingerprint templates.

        :return: None
        """
        self.send_command(CMD_DATA_WRRQ, data=bytearray.fromhex('0107000200000000000000'))
        print_h(self.recv_long_reply())