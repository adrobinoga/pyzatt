#!/usr/bin/python3.5
import time
from utils import *
import pyzk.pyzk as pyzk
import pyzk.zkmodules.defs as defs

"""
Test script to test/show several functions of the terminal spec/lib.

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

# connection
print_header("1.Read all user info")
print_info("First, connect to the device and then disable the device")
z.connect_net(ip_address, machine_port)
z.disable_device()

print_info("Get fp templates")
z.read_all_fptmp()

z.enable_device()
z.disconnect()
