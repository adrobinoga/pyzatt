#!/usr/bin/python3.5
import time
from utils import *
import pyzk.pyzk as pyzk
import pyzk.zkmodules.defs as defs

"""
Test script to test/show several functions of the "other" spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that would
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

time.sleep(0)  # sometimes a delay is useful to se

ip_address = '192.168.19.152'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)

# connection
print_header("1. Enrolling a user")

# parameters for enrolling procedure
user_id = "123999888"
finger_index = 9
fp_flag = 1

print_info("Enrolling user:")
print_info("User ID = ", user_id)
print_info("Finger index = ", finger_index)
print_info("Fingerprint type = ", fp_flag)

print_info("If the given fingerprint exists, then delete it")
if z.fp_exists(user_id, finger_index):
    print_info("Deleting fingerprint")
    z.delete_fp(user_id, finger_index)

if z.start_enroll(user_id, finger_index, fp_flag):
    print("Enrolling was successful")
else:
    print("Something went wrong")

z.disconnect()
