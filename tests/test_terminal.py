#!/usr/bin/env python

import datetime
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as defs
import pyzatt.misc as misc

"""
Test script to test/show several functions of the terminal spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


def test_terminal(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()

    misc.print_header("TEST OF TERMINAL FUNCTIONS")

    # connection
    misc.print_header("1.Connection Test")
    misc.print_info("First, connect to the device and then disable the device")
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    # get/set time
    misc.print_header("2.Set/Get time test")
    misc.print_info("The time is ")

    misc.print_info("Get current time")
    print(z.get_device_time())
    misc.print_info("Set a new time")
    z.set_device_time(datetime.datetime(2018, 1, 1, 18, 17, 16))
    print(z.get_device_time())
    misc.print_info("Set the time to now")
    z.set_device_time(datetime.datetime.now())
    print(z.get_device_time())

    # get status
    misc.print_header("3.Get status test")
    misc.print_info("You may request all the values")
    stat_keys = defs.get_status_keys()
    res = z.get_device_status(dict(zip(stat_keys, [-1]*len(stat_keys))))
    for k in res:
        print("{0} = {1}".format(k, res[k]))

    misc.print_info("Or maybe just request a couple,"
                    " but in both cases the machine"
                    " reply has all the fields")
    res = z.get_device_status({'attlog_count': -1,
                               'user_count': -1,
                               'admin_count': -1})
    for k in res:
        print("{0} = {1}".format(k, res[k]))

    misc.print_info("So you may read the fields of a"
                    " previously requested status,"
                    " using the read_status function")
    res = z.read_status(defs.STATUS['pwd_count'])
    print("{0} = {1}".format('pwd_count', res))

    # get more params
    misc.print_header("4.Device info test")

    misc.print_info("Some parameter requests:")

    print('Vendor = ' + z.get_vendor())
    print('Product code = |{0}|'.format(z.get_product_code()))
    print('Product time = |{0}|'.format(z.get_product_time()))
    print('card function = |{0}|'.format(z.get_cardfun()))
    print('User max id width = |{0}|'.format(z.get_device_info('~PIN2Width')))
    print('Firmware version = |{0}|'.format(z.get_firmware_version()))

    misc.print_info("Some write operations:")
    misc.print_info("Changing lock timer:")
    print('Original value = |{0}|'.format(z.get_device_info('LockOn')))
    z.set_device_info('LockOn', '8')
    print('New value = |{0}|'.format(z.get_device_info('LockOn')))
    z.set_device_info('LockOn', '5')
    print('Back to default value = |{0}|'.format(z.get_device_info('LockOn')))

    # get state
    misc.print_header("5.Get device state")
    print('Device state = |{0}|'.format(z.get_device_state()))

    # finally enable the device and terminate the connection
    z.enable_device()
    z.disconnect()
