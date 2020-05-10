import struct
import pyzatt.zkmodules.defs as DEFS

"""
This file contains the functions related to manage access settings
in attendance devices.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class AccessMixin:
    def get_user_group(self, user_id):
        """
        Requests the group of a given user.

        :param user_id: String, user's ID.
        :return: Integer, group number to which the user belongs.
        """
        user_sn = self.id_to_sn(user_id)
        self.send_command(cmd=DEFS.CMD_USERGRP_RRQ,
                          data=struct.pack('<I', user_sn))
        self.recv_reply()
        return self.last_payload_data[0]

    def set_user_group(self, user_id, group_no):
        """
        Sets the group of a given user.

        :param user_id: String, user's ID.
        :param group_no: Integer, new group of the user.
        :return:
        """
        user_sn = self.id_to_sn(user_id)
        grp_chg = bytearray(struct.pack('<I', user_sn)+bytes([group_no]))
        self.send_command(cmd=DEFS.CMD_USERGRP_WRQ, data=grp_chg)
        self.recv_reply()
        self.refresh_data()

    def get_tz_info(self, tz_no):
        """
        Requests a timezone.

        :param tz_no: Integer, timezone number.
        :return: List of lists, with the format
            [[T0,T1,T2,T4], [T0,T1,T2,T4], ... ].

            Where the top list consists of seven elements,
            one for each day, and each day list has 4 elements,
            that store the timezone for each day:

            (Start hour):(Start minute) To (End hour):(End minute)

            Where hours and minutes are given directly as integers.
        """
        self.send_command(cmd=DEFS.CMD_TZ_RRQ, data=struct.pack('<I', tz_no))
        self.recv_reply()

        # if the tz doesn't exists return None
        if not self.recvd_ack():
            return None

        tz_info = []

        for day in range(7):
            tz_seg = list(self.last_payload_data[2+day*4:2+((1+day)*4)])
            tz_info += [tz_seg]

        return tz_info

    def set_tz_info(self, tz_no, tz_info):
        """
        Set/create a timezone.

        :param tz_no: Integer, timezone number.
        :param tz_info: List of lists, see get_tz_info().
        :return: None.
        """
        new_tz_info = bytearray()
        new_tz_info.extend(struct.pack('<I', tz_no))
        tz_arr = []
        for day in range(7):
            tz_seg = tz_info[day]
            tz_arr += tz_seg
        new_tz_info.extend(tz_arr)
        self.send_command(cmd=DEFS.CMD_TZ_WRQ, data=new_tz_info)
        self.recv_reply()
        self.refresh_data()

    def get_unlock_comb(self, comb_no):
        """
        Request an unlock combination.

        :param comb_no: Integer, combination number.
        :return: List, with groups numbers for the given combination, the
            length of the list is the same as the number of groups for the
            combination, i.e. 2 valid groups will be returned
            as a list of two integers.
        """
        rreq_ulg = bytearray()
        rreq_ulg.append(comb_no)
        rreq_ulg.extend([0x00]*8)
        self.send_command(cmd=DEFS.CMD_ULG_RRQ, data=rreq_ulg)
        self.recv_reply()
        ulg_comb = []
        for n in range(struct.unpack('<H', self.last_payload_data[6:8])[0]):
            ulg_comb += [self.last_payload_data[1+n]]
        return ulg_comb

    def set_unlock_comb(self, comb_no, ulg_comb):
        """
        Set/create an unlock combination.

        :param comb_no: Integer, combination number.
        :param ulg_comb: List, see get_unlock_comb().
        :return: None.
        """
        wreq_ulg = bytearray([0x00]*8)
        wreq_ulg[0] = comb_no
        wreq_ulg[6:8] = struct.pack('<H', len(ulg_comb))

        for n in range(len(ulg_comb)):
            wreq_ulg[1+n] = ulg_comb[n]

        self.send_command(cmd=DEFS.CMD_ULG_WRQ, data=wreq_ulg)
        self.recv_reply()
        self.refresh_data()

    def get_group_info(self, group_no):
        """
        Get group parameters.

        :param group_no: Integer, group number.
        :return: List [Integer, [Integer]*3, Integer, Integer],
            Where the elements of the list are:

            - The group number.
            - List of timezones.
            - Verification style of the group.
            - Holidays flag, (1=valid holidays, 0=no change on holidays).
        """
        grp_req = bytearray([0x00]*8)
        grp_req[0] = group_no

        self.send_command(cmd=DEFS.CMD_GRPTZ_RRQ, data=grp_req)
        self.recv_reply()

        group_tzs = []
        for n in range(3):
            tz = [struct.unpack('<H',
                                self.last_payload_data[1+(2*n):3+(2*n)])[0]]
            if tz != 0:
                group_tzs += tz

        group_verify_style = self.last_payload_data[7] & 0x0F
        group_holidays_flg = self.last_payload_data[7] & 0x80

        return [group_no, group_tzs, group_verify_style, group_holidays_flg]

    def set_group_info(self, group_info):
        """
        Set/create group.

        :param group_info: List with new group's info, see get_group_info().
        :return: None.
        """
        wreq_grp_info = bytearray([0x00]*8)
        wreq_grp_info[0] = group_info[0]

        for n in range(len(group_info[1])):
            wreq_grp_info[1+2*n: 3+2*n] =\
                struct.pack('<H', group_info[1][n])

        wreq_grp_info[7] = group_info[2] | group_info[3]

        self.send_command(cmd=DEFS.CMD_GRPTZ_WRQ, data=wreq_grp_info)
        self.recv_reply()
        self.refresh_data()

    def get_user_tzs(self, user_id):
        """
        Get user's timezones.

        :param user_id: String, user's ID.
        :return: List of integers with the user's timezones, the list varies
            in length, if the user has only one timezone, the list has only one
            integer, if the user is using group's timezones, the list is empty.
        """
        user_sn = self.id_to_sn(user_id)
        self.send_command(cmd=DEFS.CMD_USERTZ_RRQ,
                          data=struct.pack('<I', user_sn))
        self.recv_reply()

        user_tzs = []
        if self.last_payload_data[0] == 0:
            return user_tzs

        for n in range(3):
            tz = struct.unpack('<H',
                               self.last_payload_data[2+n*2:2+((n+1)*2)])[0]
            if tz:
                user_tzs += [tz]
        return user_tzs

    def set_user_tzs(self, user_id, tzs):
        """
        Set user's timezones.

        :param user_id: String, user's ID.
        :param tzs: Lis of integers with the new user's timezones, see
            get_user_tzs().
        :return: None.
        """
        user_sn = self.id_to_sn(user_id)
        new_tz = bytearray([0x00]*20)
        new_tz[0:4] = struct.pack('<I', user_sn)
        if len(tzs) != 0:
            new_tz[4:8] = struct.pack('<I', 1)

        for n in range(len(tzs)):
            new_tz[8+(4*n):16+(4*n)] = struct.pack('<I', tzs[n])

        self.send_command(cmd=DEFS.CMD_USERTZ_WRQ, data=new_tz)
        self.recv_reply()
        self.refresh_data()

    def disable_user_tzs(self, user_id):
        """
        Make user use group's timezones.

        :param user_id: String, user's ID.
        :return: None.
        """
        self.set_user_tzs(user_id, [])

    def door_unlock(self, delay):
        """
        Unlocks the door for a given delay.

        :param delay: Integer, number of seconds to unlock the door.
        :return: None.
        """
        self.send_command(cmd=DEFS.CMD_UNLOCK, data=struct.pack('<I', delay))
        self.recv_reply()

    def get_door_state(self):
        """
        Get door state.

        :return: Integer, door state.
        """
        self.send_command(id=DEFS.CMD_DOORSTATE_RRQ)
        self.recv_reply()
        return self.last_payload_data[0]
