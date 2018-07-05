import pyzk.zkmodules.packet as zpacket
import pyzk.zkmodules.data_user as zdata_user
import pyzk.zkmodules.data_record as zdata_record
import pyzk.zkmodules.terminal as zterminal
import pyzk.zkmodules.access as zaccess
import pyzk.zkmodules.realtime as zrealtime
import pyzk.zkmodules.other as zother

"""
Main library file, defines class ZK session to access a device, the

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


class ZKSS(zpacket.PacketMixin, zdata_user.DataUserMixin,
           zdata_record.DataRecordMixin, zterminal.TerminalMixin,
           zaccess.AccessMixin, zrealtime.RealtimeMixin, zother.OtherMixin):

    def __init__(self):
        self.reply_number = 0
        self.session_id = 0
        self.connected_flg = False
        self.dev_platform = ""
        self.firmware_v = ""
