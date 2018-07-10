#!/usr/bin/python3.5
import time
import datetime
from utils import *
import pyzk.pyzk as pyzk
import pyzk.zkmodules.defs as defs

"""
Test script to test/show several functions of the data-record spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

time.sleep(0)  # sometimes a delay is useful to se

ip_address = '192.168.19.152'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()

print_header("TEST OF DATA-RECORD FUNCTIONS")

print_header("1.Read attendance log test")
print_info("First, connect to the device and then disable the device")
z.connect_net(ip_address, machine_port)
z.disable_device()

z.read_att_log()
z.print_attlog()

# print_info("Clear attendance log")
# z.clear_att_log()
# z.read_att_log()
# z.print_attlog()

print_header("2.Read operation log test")
z.read_op_log()
z.print_oplog()

# print_info("Clear operation log")
# z.clear_log()
# z.read_op_log()
# z.print_oplog()

# finally enable the device and terminate the connection
z.enable_device()
z.disconnect()

