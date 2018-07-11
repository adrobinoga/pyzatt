#!/usr/bin/python3.5
import time
import os.path
from utils import *
import pyzk.pyzk as pyzk
from pyzk.zkmodules.defs import *

"""
Test script to clear data on the machine

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

time.sleep(0)

ip_address = '192.168.19.152'  # set the ip address of the device to test
machine_port = 4370

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)
z.disable_device()

print_header("Clear data")

z.clear_data(5)

z.enable_device()
z.disconnect()
