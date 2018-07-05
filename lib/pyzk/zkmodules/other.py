from pyzk.zkmodules.defs import *

"""
This file contains the functions related to the other procedures listed
on the protocol spec.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


class OtherMixin:

    def enable_device(self):
        """
        Enables the device, puts the machine in normal operation.

        :return: Bool, returns True if the device acknowledges
        the enable command.
        """
        self.send_command(CMD_ENABLEDEVICE)
        self.recv_reply()
        return self.recvd_ack()

    def disable_device(self):
        """
        Disables the device, disables the fingerprint, keyboard
        and RF card modules.

        :return: Bool, returns True if the device acknowledges
        the disable command.
        """
        self.send_command(CMD_DISABLEDEVICE)
        self.recv_reply()
        return self.recvd_ack()
