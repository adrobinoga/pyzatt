#!/usr/bin/env python

import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt

"""
Test script to enable the machine

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


def test_enable(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    misc.print_header("Eneabling device")

    z.enable_device()
    z.disconnect()
