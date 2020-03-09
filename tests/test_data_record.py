#!/usr/bin/env python

import pytest
import time
import datetime
from pyzatt.misc import *
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as defs

"""
Test script to test/show several functions of the data-record spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""


def test_data_record(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()

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

