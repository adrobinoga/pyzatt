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

def enroll(id, fp_idx, fp_flag):
    print_info("Enrolling user:")
    print("User ID = ", id)
    print("Finger index = ", fp_idx)
    print("Fingerprint type = ", fp_flag)

    print_info("Delete previous fingerprint")
    z.delete_fp(id, fp_idx)

    print_info("Ready to enroll!")
    if z.enroll_user(id, fp_idx, fp_flag):
        print("Enrolling was successful")
        print_info("After enrolling")
        z.read_all_user_id()
        z.read_all_fptmp()
        z.print_users_summary()
        input("Press ENTER")

    else:
        print("Something went wrong")

time.sleep(0)  # sometimes a delay is useful to se

ip_address = '192.168.19.152'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)

print_header("1. Enrolling a users fingerprints")

print_info("Before enrolling users")
z.refresh_data()
z.read_all_user_id()
z.read_all_fptmp()
z.print_users_summary()

print_info("Enrolling User 1")
enroll(id='8888', fp_idx=4, fp_flag=1)

print_info("Enrolling User 2")
enroll(id='9999', fp_idx=6, fp_flag=1)

print_info("After enrolling users")
z.refresh_data()
z.read_all_user_id()
z.read_all_fptmp()
z.print_users_summary()

z.enable_device()
z.disconnect()
