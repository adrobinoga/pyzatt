import struct
import pyzatt.zkmodules.defs as DEFS

"""
This file contains the functions to extract info of realtime events
incoming from attendance devices.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class RealtimeMixin:

    def enable_realtime(self):
        """
        Sends command to enable realtime events.

        :return: None.
        """
        self.send_command(cmd=DEFS.CMD_REG_EVENT,
                          data=bytearray([0xff, 0xff, 0x00, 0x00]))
        self.recv_reply()

    def get_last_event(self):
        """
        Returns the last event code.

        :return: Integer, last event code(as given on the session id field).
        """
        return self.last_event_code

    def parse_alarm_type(self):
        """
        Extracts the alarm type of the last event.

        :return: Integer, alarm type, if it fails to extract the alarm type,
            returns -1.
        """
        alarm_type = -1
        if self.last_event_code == DEFS.EF_ALARM:
            alarm_type = struct.unpack('<I', self.last_payload_data[0:4])[0]
        return alarm_type

    def parse_duress_alarm(self):
        """
        Extracts info from an alarm event packet.

        :return: List [Integer, Integer, Integer].

            Where the elements of the list are:

            1. Alarm type.
            2. User's index.
            3. Matching way.

            If it fails tos extract those fields, returns a
            list of -1 values [-1,-1,-1].
        """
        alarm_type = -1
        sn = -1
        match_type = -1
        if self.last_event_code == DEFS.EF_ALARM:
            alarm_type = struct.unpack('<H', self.last_payload_data[4:6])[0]
            sn = struct.unpack('<H', self.last_payload_data[6:8])[0]
            match_type = struct.unpack('<I', self.last_payload_data[8:12])[0]
        return [alarm_type, sn, match_type]

    def parse_event_attlog(self):
        """
        Extracts info from a attendance event.

        :return: List [Str, Integer, Str].
            Where the elements of the list are:

            1. User's ID.
            2. Verification type, (password=0, fp=1, rfid=2).
            3. Date string, with the format yyyy/mm/dd HH:MM:SS.

            If it fails to extract these values, returns ['',-1,''].
        """
        uid = ''
        ver_type = -1
        date_str = ''
        if self.last_event_code == DEFS.EF_ATTLOG:
            uid = self.last_payload_data[0:9].decode('ascii').\
                replace('\x00', '')
            ver_type = struct.unpack('<H', self.last_payload_data[24:26])[0]
            date_str = "20%i/%i/%i %i:%i:%i" %\
                       tuple(self.last_payload_data[26:32])

        return [uid, ver_type, date_str]

    def parse_event_enroll_fp(self):
        """
        Extracts info from an enrolled fingerprint event.

        :return: List [Bool, Str, Integer, Integer].
            Where the elements of the list are:

            1. Enroll result, True if it was successful.
            2. User ID.
            3. Finger index of the fingerprint.
            4. Fingerprint template size.

            If it fails to extract these values, returns [False,'',-1,-1].
        """
        uid = ''
        fp_idx = -1
        fp_size = -1
        enroll_flg = False

        if self.last_event_code == DEFS.EF_ENROLLFINGER:
            enroll_flg = True if \
                struct.unpack('<H', self.last_payload_data[0:2])[0] == 0\
                else False

            uid = self.last_payload_data[4:13].decode('ascii').\
                replace('\x00', '')

            fp_idx = self.last_payload_data[13]

            fp_size = struct.unpack('<H', self.last_payload_data[2:4])[0]

        return [enroll_flg, uid, fp_idx, fp_size]

    def parse_score_fp_event(self):
        """
        Extracts the score of a given fingerprint sample in a enrolling
        procedure.

        :return: Integer, the score may be 100(valid) or 0(invalid),
            returns -1 if it fails to extract the score.
        """
        score = -1
        if self.last_event_code == DEFS.EF_FPFTR:
            score = self.last_payload_data[0]
        return score

    def wait_for_fingerscore(self):
        """
        Blocks execution until a finger score event is received.

        :return: Integer, the score may be 100(valid) or 0(invalid),
            returns -1 if it fails to extract the score.
        """
        while True:
            self.recv_event()
            if self.last_event_code == DEFS.EF_FPFTR:
                return self.parse_score_fp_event()

    def parse_verify_event(self):
        """
        Extracts the user index from a verify event packet.

        :return: Integer, user internal index on machine, returns -1 if it
            the packet doesn't correspond to a EF_VERIFY event.
        """
        user_sn = -1
        if self.last_event_code == DEFS.EF_VERIFY:
            user_sn = struct.unpack('<I', self.last_payload_data[0:4])[0]

            if self.last_payload_data[4] != 1:
                print('Found value different of 1 on verify packet: %' %
                      (self.last_payload_data[4]))

        return user_sn
