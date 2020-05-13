import struct
import pyzatt.zkmodules.defs as DEFS

"""
This file contains the functions related to the other procedures listed
on the protocol spec.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class OtherMixin:

    def enable_device(self):
        """
        Enables the device, puts the machine in normal operation.

        :return: Bool, returns True if the device acknowledges
            the enable command.
        """
        self.send_command(DEFS.CMD_ENABLEDEVICE)
        self.recv_reply()
        return self.recvd_ack()

    def disable_device(self, timer=None):
        """
        Disables the device, disables the fingerprint, keyboard
        and RF card modules.

        :param timer: Integer, disable timer, if it is omitted, an enable
            command must be send to make the device return to normal operation.
        :return: Bool, returns True if the device acknowledges
            the disable command.
        """
        if timer:
            self.send_command(DEFS.CMD_DISABLEDEVICE, struct.pack('<I', timer))
        else:
            self.send_command(DEFS.CMD_DISABLEDEVICE)

        self.recv_reply()
        return self.recvd_ack()

    def clear_admins(self):
        """
        Clears the privileges of all the users, they are set
        to default "common user".

        :return: Bool, returns True if the device acknowledges
            the command.
        """
        self.send_command(DEFS.CMD_CLEAR_ADMIN)
        self.recv_reply()
        return self.recvd_ack()

    def poweroff(self):
        """
        Sends the poweroff command and closes the connection.

        :return: None.
        """
        self.send_command(DEFS.CMD_POWEROFF)
        self.recv_reply()
        self.send_command(DEFS.CMD_EXIT)
        self.recv_reply()

    def restart(self):
        """
        Restarts the devices and closes the connections.

        :return: None.
        """
        self.send_command(DEFS.CMD_RESTART)
        self.soc_zk.close()

    def enroll_user(self, user_id, finger_index, fp_flag=1):
        """
        Enrolls a fingerprint.

        :param user_id: String, users id, it may be a work id or personal id.
        :param finger_index: Int, index of the fingerprint to enroll.
        :param fp_flag: Int, 1(default) sets to valid, 3 sets a duress fp.
        :return: Bool, if the enrolling process was successful.
        """
        # check the with of the user's id
        pwidth = self.get_pinwidth()
        if len(user_id) > pwidth:
            return False

        self.cancel_capture()

        # data of payload for enroll command
        enroll_dat = bytearray([0x00]*26)
        enroll_dat[0:len(user_id)] = user_id.encode()
        enroll_dat[24] = finger_index
        enroll_dat[25] = fp_flag

        self.send_command(DEFS.CMD_STARTENROLL, enroll_dat)
        self.recv_reply()

        # send verify command
        self.start_identify()

        # inits figerprint counter
        fp_samples = 0

        # perform 3 samples of the fingerprint
        while fp_samples < 3:
            score = self.wait_for_fingerscore()
            # if one sample it isn't of good quality the process finishes
            if score != 100:
                return False
            fp_samples += 1

        # receive enroll result
        self.recv_event()

        if self.last_event_code == DEFS.EF_ENROLLFINGER:
            result = struct.unpack('<H', self.last_payload_data[0:2])[0]
            # fp_size = struct.unpack('<H', self.last_payload_data[2:4])[0]
            # user_id_reply = self.last_payload_data[4:13].decode('ascii')
            # finger_index_reply = self.last_payload_data[13]
            return not result

    def start_identify(self):
        """
        Sends the verify command and receives the reply.

        :return: Bool, returns True if the device acknowledges
            the command.
        """
        self.send_command(DEFS.CMD_STARTVERIFY)
        self.recv_reply()
        return self.recvd_ack()

    def cancel_capture(self):
        """
        Sends the cancel capture command and receives the reply.

        :return: Bool, returns True if the device acknowledges
            the command.
        """
        self.send_command(DEFS.CMD_CANCELCAPTURE)
        self.recv_reply()
        return self.recvd_ack()
