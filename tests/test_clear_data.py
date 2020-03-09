#!/usr/bin/env python

import pytest
import time
from pyzatt.misc import *
import pyzatt.pyzatt as pyzatt
from pyzatt.zkmodules.defs import *

"""
Test script to clear data on the machine

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

@pytest.mark.skip()
@pytest.mark.destructive
def test_clear_data(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test

    machine_port = 4370

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    print_header("Clear data")

    z.clear_data(5)

    z.enable_device()
    z.disconnect()
