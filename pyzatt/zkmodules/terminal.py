import socket
import struct
import pyzatt.zkmodules.defs as DEFS
import pyzatt.misc as misc

"""
This file contains the functions of the "terminal" protocol spec
in attendance devices.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


class TerminalMixin:

    def connect_net(self, ip_addr, dev_port):
        """
        Connects to the machine, sets the socket connection and inits session
        by sending the connect command.

        :param ip_addr: String, ip address of the device.
        :param dev_port: Int, port number.
        :return: Bool, returns True if connection is successful,
            otherwise it returns False, also sets
            the flag self.connected_flg if
            the connection is successful.
        """

        # connects to machine
        self.soc_zk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_zk.connect((ip_addr, dev_port))

        # send connect command
        self.send_command(DEFS.CMD_CONNECT)

        # receive reply
        self.recv_reply()

        # sets session id
        self.session_id = self.last_session_code

        # set SDKBuild variable of the device
        self.set_device_info('SDKBuild', '1')

        # check reply code
        self.connected_flg = self.recvd_ack()
        return self.connected_flg

    def disconnect(self):
        """
        Terminates connection with the given device.

        :return: Bool, returns True if disconnection command was
            processed successfully, also clears the flag self.connected_flg.
        """
        # terminate connection command
        self.send_command(DEFS.CMD_EXIT)
        self.recv_reply()

        # close connection and update flag
        self.soc_zk.close()
        self.connected_flg = False

        return self.recvd_ack()

    def get_device_time(self):
        """
        Requests and returns the decoded time of the device.

        :return: Datetime object, datetime of the device.
        """
        self.send_command(DEFS.CMD_GET_TIME)
        self.recv_reply()
        return misc.decode_time(self.last_payload_data)

    def set_device_time(self, t=misc.datetime.datetime.now()):
        """
        Sets the time of the device.

        :param t: Datetime object, new time of the device, if not specified,
            it defaults to current time.
        :return: Bool, returns True if set time command was
            processed successfully.
        """
        self.send_command(DEFS.CMD_SET_TIME, data=misc.encode_time(t))
        self.recv_reply()
        return self.recvd_ack()

    def get_device_status(self, stat_keys):
        """
        Requests the status structure of the device and returns the status
        values in the given dictionary.

        :param stat_keys: Dictionary, with the keys to request, the values
            of the given keys are overwritten with the output values.

            Example: {admin_count: -1, user_count: -1}.

        :return: Dictionary, the output is given on the same input dict.
        """
        # request status structure
        self.send_command(DEFS.CMD_GET_FREE_SIZES)

        self.recv_reply()
        self.dev_status = self.last_payload_data

        # read the requested fields from the structure
        # iterates through the given keys
        for k in stat_keys:
            # reads the field and stores the result in the given dict
            try:
                stat_keys[k] = self.read_status(DEFS.STATUS[k])
            except struct.error:
                print("Failed to read field: {0}".format(k))
                stat_keys[k] = -1

        return stat_keys

    def read_status(self, p):
        """
        Reads a field from the device status attribute(self.dev_status).

        :param p: Position to read, to get the position is recommended to
            use STATUS[<key>], where key should be the name of a valid field of
            the status structure.
        :return: Integer, stored in the given position.
        """
        return struct.unpack('<I', self.dev_status[p: p + 4])[0]

    def read_attlog_count(self):
        """
        Returns the number of attendance entries.

        :return: Integer, attendance counter.
        """
        return self.read_status(DEFS.STATUS['attlog_count'])

    def read_user_count(self):
        """
        Returns the number of registered users.

        :return: Integer, user count.
        """
        return self.read_status(DEFS.STATUS['user_count'])

    def get_device_info(self, param_name):
        """
        Command to request a given parameter from the device.

        :param param_name: String, parameters to request, see the protocol
            terminal spec to see a list of valid param names.
        :return: String, the param value, if it is a boolean, it may be given
            as "0" or "1", integers are given as strings.
        """
        # request a parameter
        self.send_command(DEFS.CMD_OPTIONS_RRQ,
                          bytearray("{0}\x00".format(param_name), 'ascii'))
        self.recv_reply()
        # extract and returns the reply value
        return self.last_payload_data.decode('ascii').split('=')[-1]

    def set_device_info(self, param_name, new_value):
        """
        Sets a parameter of the device.

        :param param_name: String, parameter to modify, see the protocol
            terminal spec to see a list of valid param names and valid values.
        :param new_value: String, the new value of the parameters, if it is a
            boolean, it may be given as "0" or "1",
            integers are given as strings.
        :return: Bool, returns True if the commands were
            processed successfully.
        """
        self.send_command(DEFS.CMD_OPTIONS_WRQ, bytearray(
            "{0}={1}\x00".format(param_name, new_value), 'ascii'))
        self.recv_reply()
        ack1 = self.recvd_ack()
        self.send_command(DEFS.CMD_REFRESHOPTION)
        self.recv_reply()
        ack2 = self.recvd_ack()
        return ack1 and ack2

    def get_serial_number(self):
        """
        Returns the serial number of the device.

        :return: String, serial number.
        """
        return self.get_device_info("~SerialNumber")

    def get_product_code(self):
        """
        Returns the product code(device name).

        :return: String, device name.
        """
        return self.get_device_info("~DeviceName")

    def get_cardfun(self):
        """
        Returns the RFCardOn flag.

        :return: String, RFCardOn flag, it may be "0" or "1".
        """
        self.get_device_info("~IsOnlyRFMachine")
        return self.get_device_info("~RFCardOn")

    def get_vendor(self):
        """
        Returns the vendor name.

        :return: String.
        """
        return self.get_device_info("~OEMVendor")

    def get_product_time(self):
        """
        Requests the fabrication time.

        :return: String.
        """
        return self.get_device_info("~ProductTime")

    def get_platform(self):
        """
        Returns the plaform name.

        :return: String.
        """
        return self.get_device_info("~Platform")

    def get_pinwidth(self):
        """
        Requests the max size of the user ID field.

        :return: Integer, allowed size for users ID.
        """
        return int(self.get_device_info('~PIN2Width').replace('\x00', ''))

    def get_firmware_version(self):
        """
        Returns the firmware version.

        :return: String.
        """
        self.send_command(DEFS.CMD_GET_VERSION)
        self.recv_reply()
        return self.last_payload_data.decode('ascii')

    def get_device_state(self):
        """
        Request the device state, see the protocol spec to check
        for state codification.

        :return: Integer, ranges from 0 to 5.
        """
        self.send_command(DEFS.CMD_STATE_RRQ)
        self.recv_reply()
        return self.last_session_code
