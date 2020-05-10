
"""
This file contains definition of constants and codes used for the protocol
implementation.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""

# fixed arrays
START_TAG = bytearray([0x50, 0x50, 0x82, 0x7D])
SHORT_ZERO = bytearray([0x00]*2)

# command codes
CMD_CONNECT = 0x03e8
CMD_EXIT = 0x03e9
CMD_ENABLEDEVICE = 0x03ea
CMD_DISABLEDEVICE = 0x03eb
CMD_RESTART = 0x03ec
CMD_POWEROFF = 0x03ed
CMD_SLEEP = 0x03ee
CMD_RESUME = 0x03ef
CMD_CAPTUREFINGER = 0x03f1
CMD_TEST_TEMP = 0x03f3
CMD_CAPTUREIMAGE = 0x03f4
CMD_REFRESHDATA = 0x03f5
CMD_REFRESHOPTION = 0x03f6
CMD_TESTVOICE = 0x03f9
CMD_GET_VERSION = 0x044c
CMD_CHANGE_SPEED = 0x044d
CMD_AUTH = 0x044e
CMD_PREPARE_DATA = 0x05dc
CMD_DATA = 0x05dd
CMD_FREE_DATA = 0x05de
CMD_DATA_WRRQ = 0x05df
CMD_DATA_RDY = 0x05e0
CMD_DB_RRQ = 0x0007
CMD_USER_WRQ = 0x0008
CMD_USERTEMP_RRQ = 0x0009
CMD_USERTEMP_WRQ = 0x000a
CMD_OPTIONS_RRQ = 0x000b
CMD_OPTIONS_WRQ = 0x000c
CMD_ATTLOG_RRQ = 0x000d
CMD_CLEAR_DATA = 0x000e
CMD_CLEAR_ATTLOG = 0x000f
CMD_DELETE_USER = 0x0012
CMD_DELETE_USERTEMP = 0x0013
CMD_CLEAR_ADMIN = 0x0014
CMD_USERGRP_RRQ = 0x0015
CMD_USERGRP_WRQ = 0x0016
CMD_USERTZ_RRQ = 0x0017
CMD_USERTZ_WRQ = 0x0018
CMD_GRPTZ_RRQ = 0x0019
CMD_GRPTZ_WRQ = 0x001a
CMD_TZ_RRQ = 0x001b
CMD_TZ_WRQ = 0x001c
CMD_ULG_RRQ = 0x001d
CMD_ULG_WRQ = 0x001e
CMD_UNLOCK = 0x001f
CMD_CLEAR_ACC = 0x0020
CMD_CLEAR_OPLOG = 0x0021
CMD_OPLOG_RRQ = 0x0022
CMD_GET_FREE_SIZES = 0x0032
CMD_ENABLE_CLOCK = 0x0039
CMD_STARTVERIFY = 0x003c
CMD_STARTENROLL = 0x003d
CMD_CANCELCAPTURE = 0x003e
CMD_STATE_RRQ = 0x0040
CMD_WRITE_LCD = 0x0042
CMD_CLEAR_LCD = 0x0043
CMD_GET_PINWIDTH = 0x0045
CMD_SMS_WRQ = 0x0046
CMD_SMS_RRQ = 0x0047
CMD_DELETE_SMS = 0x0048
CMD_UDATA_WRQ = 0x0049
CMD_DELETE_UDATA = 0x004a
CMD_DOORSTATE_RRQ = 0x004b
CMD_WRITE_MIFARE = 0x004c
CMD_EMPTY_MIFARE = 0x004e
CMD_VERIFY_WRQ = 0x004f
CMD_VERIFY_RRQ = 0x0050
CMD_TMP_WRITE = 0x0057
CMD_CHECKSUM_BUFFER = 0x0077
CMD_DEL_FPTMP = 0x0086
CMD_GET_TIME = 0x00c9
CMD_SET_TIME = 0x00ca
CMD_REG_EVENT = 0x01f4

# reply codes
CMD_ACK_OK = 0x07d0
CMD_ACK_ERROR = 0x07d1
CMD_ACK_DATA = 0x07d2
CMD_ACK_RETRY = 0x07d3
CMD_ACK_REPEAT = 0x07d4
CMD_ACK_UNAUTH = 0x07d5
CMD_ACK_UNKNOWN = 0xffff
CMD_ACK_ERROR_CMD = 0xfffd
CMD_ACK_ERROR_INIT = 0xfffc
CMD_ACK_ERROR_DATA = 0xfffb

# realtime event codes
EF_ATTLOG = 0x1
EF_FINGER = 0x2
EF_ENROLLUSER = 0x4
EF_ENROLLFINGER = 0x8
EF_BUTTON = 0x10
EF_UNLOCK = 0x20
EF_VERIFY = 0x80
EF_FPFTR = 0x100
EF_ALARM = 0x200

# status positions
STATUS = \
    {
        'admin_count': 48,
        'user_count': 16,
        'fp_count': 24,
        'pwd_count': 52,
        'oplog_count': 40,
        'attlog_count': 32,
        'fp_capacity': 56,
        'user_capacity': 60,
        'attlog_capacity': 64,
        'remaining_fp': 68,
        'remaining_user': 72,
        'remaining_attlog': 76,
        'face_count': 80,
        'face_capacity': 88
    }


def get_status_keys():
    """
    Returns the list of status variable names.

    :return: List of strings, with the status field names.
    """
    return STATUS.keys()


# verification styles
GROUP_VERIFY = 0
FPorPWorRF = 0x80
FP = 0x81
PIN = 0x82
PW = 0x83
RF = 0x84
FPorPW = 0x85
FPorRF = 0x86
PWorRF = 0x87
PINandFP = 0x88
FPandPW = 0x89
FPandRF = 0x8a
PWandRF = 0x8b
FPandPWandRF = 0x8c
PINandFPandPW = 0x8d
FPandRForPIN = 0x8e
