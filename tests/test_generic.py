#!/usr/bin/env python

import pytest
import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt

"""
Generic test

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


@pytest.mark.skip(reason="WIP")
def test_generic(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    misc.print_header("Put your header here")

    z.enable_device()
    z.disconnect()
