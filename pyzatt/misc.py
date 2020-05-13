import binascii
import struct
import datetime
from colorama import Fore, Style

"""
This file contains several functions needed to encode and decode values, some
functions useful for debugging are also included.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


hhh = 80*'#'


def print_info(s):
    """
    Prints text in green bright font.

    :param s: String, text to be printed.
    :return: None.
    """
    print(Style.BRIGHT + Fore.GREEN + s + Style.RESET_ALL)


def print_header(s):
    """
    Prints a title in green bright font.

    :param s: String, text to be printed.
    :return: None.
    """
    print_info('\n' + hhh + '\n#\t' + s + '\n')


def print_hex(arr):
    """
    Prints a bytearray as a sequence of hex numbers, e.g. "fffe01".

    :param arr: Bytearray to print.
    :return: None.
    """
    print(binascii.hexlify(arr))


def is_valid_payload(p):
    """
    Checks if a given packet payload is valid, considering the checksum,
    where the payload is given with the checksum.

    :param p: Bytearray, with the payload contents.
    :return: Bool, if the payload is consistent, returns True,
        otherwise returns False.
    """
    # if the checksum is valid the checksum calculation, without removing the
    # checksum, should be equal to zero

    if checksum16(p) == 0:
        return True
    else:
        return False


def decode_time(enc_t_arr):
    """
    Decodes time, as given on ZKTeco get/set time commands.

    :param enc_t_arr: Bytearray, with the time field stored in little endian.
    :return: Datetime object, with the extracted date.
    """
    enc_t = struct.unpack('<I', enc_t_arr)[0]  # extracts the time value
    secs = int(enc_t % 60)  # seconds
    mins = int((enc_t / 60.) % 60)  # minutes
    hour = int((enc_t / 3600.) % 24)  # hours
    day = int(((enc_t / (3600. * 24.)) % 31)) + 1  # day
    month = int(((enc_t / (3600. * 24. * 31.)) % 12)) + 1  # month
    year = int((enc_t / (3600. * 24.)) / 365) + 2000  # year

    return datetime.datetime(year, month, day, hour, mins, secs)


def encode_time(t):
    """
    Converts date to specific codification of time used in ZKTeco
    get/set time procedures.

    :param t: Datetime object, with the date.
    :return: Bytearray, with the time stored in little endian format.
    """
    return bytearray(struct.pack('<I',
                                 ((t.year % 100) * 12 * 31 + (
                                     (t.month - 1) * 31) + t.day - 1) *
                                 (24 * 60 * 60) + (
                                     t.hour * 60 + t.minute) * 60 + t.second
                                 ))


def checksum16(payload):
    """
    Calculates checksum of packet.

    :param payload: Bytearray, data to which the checksum is going
        to be applied.
    :return: Int, checksum result given as a number.
    """

    chk_32b = 0  # accumulates short integers to calculate checksum
    j = 1  # iterates through payload

    # make odd length packet, even
    if len(payload) % 2 == 1:
        payload.append(0x00)

    while j < len(payload):
        # extract short integer, in little endian, from payload
        num_16b = payload[j - 1] + (payload[j] << 8)
        # accumulate
        chk_32b += num_16b
        j += 2  # increment pointer by 2 bytes

    # adds the two first bytes to the other two bytes
    chk_32b = (chk_32b & 0xFFFF) + ((chk_32b & 0xFFFF0000) >> 16)

    # ones complement to get final checksum
    chk_16b = chk_32b ^ 0xFFFF

    return chk_16b
