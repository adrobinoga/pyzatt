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

        :return: None. Stores the users info in the ZKUsers dict.
        """
        self.send_command(cmd=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('0109000500000000000000'))

        # receive dataset with users info
        users_dataset = self.recv_long_reply()
        total_size_dataset = len(users_dataset)

        # clear the users dict
        self.users = {}

        # skip first 4 bytes (size + zeros)
        i = 4
        while i < total_size_dataset:
            # extract serial number
            user_sn = struct.unpack('<H', users_dataset[i:i+2])[0]

            # extract permission token
            perm_token = users_dataset[i+2]

            # extract user password, if it is invalid, stores ''
            if users_dataset[i+3] != 0x00:
                password = users_dataset[i + 3:i + 11]
                # remove trailing zeros
                password = password.decode('ascii').replace('\x00', '')

            else:
                password = ''

            # extract user name
            user_name = users_dataset[i+11:i+35].decode('ascii')

            # remove non printable chars
            user_name = user_name.replace('\x00', '')

            # extract card number
            card_no = struct.unpack('<I', users_dataset[i+35:i+39])[0]

            # extract group number
            group_no = users_dataset[i+39]

            # extract user timezones if they exists
            if struct.unpack('<H', users_dataset[i+40:i+42])[0] == 1:
                user_tzs = [0]*3
                user_tzs[0] = struct.unpack('<H', users_dataset[i+42:i+44])[0]
                user_tzs[1] = struct.unpack('<H', users_dataset[i+44:i+46])[0]
                user_tzs[2] = struct.unpack('<H', users_dataset[i+46:i+48])[0]
            else:
                user_tzs = []

            # extract the user id
            user_id = users_dataset[i+48:i+57].decode('ascii')

            # remove non printable chars
            user_id = user_id.replace('\x00', '')

            # append user to the list of users
            self.add_user(user_sn)
            # set the corresponding info
            self.users[user_sn].set_user_info(
                                            user_id=user_id,
                                            user_sn=user_sn,
                                            name=user_name,
                                            password=password,
                                            card_no=card_no,
                                            admin_lv=perm_token >> 1,
                                            neg_enabled=perm_token & 1,
                                            user_group=group_no,
                                            user_tzs=user_tzs
                                            )
            # every user entry is 72 bytes long
            i += 72

    def get_verify_style(self, user_id):
        """
        Requests the verification style of a given user.

        :param user_id: Str, user's ID.
        :return: Integer, verification style.
        """
        self.send_command(cmd=CMD_VERIFY_RRQ,
                          data=struct.pack('<H', self.id_to_sn(user_id)))
        self.recv_reply()

        return self.last_payload_data[2]

    def set_verify_style(self, user_id, verify_style):
        """
        Sets the verification style of a given user.

        :param user_id: Str, user's ID.
        :param verify_style: Integer, verification style.
        :return: Bool, returns True if the command was
        processed successfully.
        """
        ver_data = bytearray([0x00]*24)
        ver_data[0:2] = struct.pack('<H', self.id_to_sn(user_id))
        ver_data[2] = verify_style
        self.send_command(cmd=CMD_VERIFY_WRQ, data=ver_data)
        self.recv_reply()
        return self.recvd_ack()

    def delete_user(self, user_id):
        """
        Deletes a given user.

        :param user_id: String, user's ID.
        :return: None.
        """
        user_sn = self.users[self.id_to_sn(user_id)].user_sn
        del_data = bytearray(struct.pack('<H', user_sn))
        self.send_command(CMD_DELETE_USER, del_data)
        self.recv_reply()
        self.refresh_data()

    def set_user_info(self, user_id, name="",
                      password="", card_no=0,
                      admin_lv=0, neg_enabled=0,
                      user_group=1, user_tzs=[1, 0, 0]):
        """
        Sets user info on corresponding ZKUser and uploads that new info.

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
        :return:None.
        """
        # check if user exists
        if self.id_exists(user_id):
            # users exists
            user_sn = self.id_to_sn(user_id)
        else:
            # user doesn't exists
            user_sn = self.create_user()

        # set the corresponding info
        self.users[user_sn].set_user_info(
            user_id=user_id,
            user_sn=user_sn,
            name=name,
            password=password,
            card_no=card_no,
            admin_lv=admin_lv,
            neg_enabled=neg_enabled,
            user_group=user_group,
            user_tzs=user_tzs
        )
        self.upload_user_info(user_id)

    def upload_user_info(self, user_id, user_info=None):
        """
        Uploads a user's info, as is on the ZKUsers list.

        :return: None.
        """
        user_sn = self.id_to_sn(user_id)

        if user_info == None:
            user_info = self.users[user_sn].ser_user()

        self.send_command(cmd=CMD_USER_WRQ, data=user_info)
        self.recv_reply()
        self.refresh_data()

    def get_password(self, user_id):
        """
        Requests the password of a given user.
        :param user_id: String, user's ID.
        :return:
        """
        user_sn = self.id_to_sn(user_id)
        return self.users[user_sn].user_password

    def clear_password(self, user_id):
        """
        Deletes the password of a given user.

        :param user_id: String, user's ID.
        :return: None.
        """
        self.set_password(user_id, "")

    def set_password(self, user_id, password):
        """
        Changes the password of a given user.

        :param user_id: String, user's ID.
        :param password: String, password (<=8 digits).
        :return: None.
        """
        user_sn = self.id_to_sn(user_id)
        self.users[user_sn].user_password = password
        user_entry = self.users[user_sn].ser_user()
        self.upload_user_info(user_id, user_entry)

    def read_all_fptmp(self):
        """
        Requests all the fingerprint templates.

        :return: None. Stores the templates and templates info in the
        corresponding ZKUsers entries.
        """
        self.send_command(cmd=CMD_DATA_WRRQ,
                          data=bytearray.fromhex('0107000200000000000000'))

        # receive the fp template dataset
        fptemplates_dataset = self.recv_long_reply()
        total_size_dataset = len(fptemplates_dataset)

        # skip first 4 bytes (size + zeros)
        i = 4
        while i < total_size_dataset:
            # extract template size
            tmp_size = struct.unpack('<H', fptemplates_dataset[i:i + 2])[0] \
                       - 6

            # extract user serial number
            user_sn = struct.unpack('<H', fptemplates_dataset[i + 2:i + 4])[0]

            # get fingerprint index
            fp_idx = fptemplates_dataset[i + 4]

            # get fingerprint flag
            fp_flg = fptemplates_dataset[i + 5]

            # extract template
            fp_tmp = fptemplates_dataset[i + 6: i + tmp_size]

            # store the template, index and type
            self.users[user_sn].set_user_fptmp(fp_index=fp_idx, fp_tmp=fp_tmp,
                                               fp_flag=fp_flg)

            # every template entry is 6 bytes + template length
            i += tmp_size+6

    def delete_fp(self, user_id, fp_index):
        """
        Delete a fingerprint template, for a given user ID and fp index.

        :param user_id: String, user's ID.
        :param fp_index: Integer, fingerprint index to be removed.
        :return: None.
        """
        # form the delete structure
        del_data = bytearray([0x00]*25)
        del_data[0:len(user_id)] = user_id.encode()
        del_data[24] = fp_index

        # send the request
        self.send_command(cmd=CMD_DEL_FPTMP, data=del_data)
        self.recv_reply()

        # refresh the device data
        self.refresh_data()

    def download_fp(self, user_id, fp_index):
        """
        Requests a fingerprint template, from a given user.

        :param user_id: Str, user's ID.
        :param fp_index: Integer, fingerprint index [0-9].
        :return: Bytearray, fingerprint template.
        """
        req_fp = bytearray()
        req_fp.extend(struct.pack('<H', self.id_to_sn(user_id)))
        req_fp.append(fp_index)

        # send request
        self.send_command(cmd=CMD_USERTEMP_RRQ, data=req_fp)
        return self.recv_long_reply()

    def upload_fp(self, user_id, fp, fp_index, fp_flag):
        """
        Upload fingerprint template data of a given user.

        :param user_id: String, user's ID.
        :param fp: Bytearray, fingerprint template.
        :param fp_index: Integer, fingerprint index.
        :param fp_flag: Integer, fingerprint flag (duress=3, valid=1).
        :return: None.
        """
        user_sn = self.id_to_sn(user_id)
        self.disable_device()

        # sending prep struct
        fp_size = struct.pack('<H', len(fp))
        prep_data = bytearray([0x00]*4)
        prep_data[0:2] = fp_size
        self.send_command(cmd=CMD_PREPARE_DATA, data=prep_data)
        self.recv_reply()

        # sending template
        self.send_command(cmd=CMD_DATA, data=fp)
        self.recv_reply()

        # request checksum
        self.send_command(cmd=CMD_CHECKSUM_BUFFER)
        self.recv_reply()  # ignored

        # send write request
        tmp_wreq_data = bytearray([0x00] * 6)
        tmp_wreq_data[0:2] = struct.pack('<H', user_sn)
        tmp_wreq_data[2] = fp_index
        tmp_wreq_data[3] = fp_flag
        tmp_wreq_data[4:6] = fp_size
        self.send_command(cmd=CMD_TMP_WRITE, data=tmp_wreq_data)
        self.recv_reply()

        # free data buffer
        self.send_command(cmd=CMD_FREE_DATA)
        self.recv_reply()

        # refresh data
        self.refresh_data()

    def refresh_data(self):
        """
        Refresh data on device (fingerprints, user info and settings).

        :return: None.
        """
        self.send_command(cmd=CMD_REFRESHDATA)
        self.recv_reply()
