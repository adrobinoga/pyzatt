#!/usr/bin/env python

import pytest
import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as DEFS

"""
Test script to test/show parsing functions of the realtime spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


@pytest.mark.skip(reason="manual test")
@pytest.mark.manual
def test_realtime(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()

    misc.print_header("TEST OF REALTIME FUNCTIONS")

    # connection
    misc.print_header("1.Realtime Test")
    z.connect_net(ip_address, machine_port)

    # read user ids
    z.disable_device()
    z.read_all_user_id()
    z.enable_device()

    # enable the report of rt packets
    z.enable_realtime()

    misc.print_info("Ready to receive events from the machine")

    try:
        while True:
            # wait for event
            z.recv_event()
            ev = z.get_last_event()

            # process the event
            print("\n"+"#"*50)
            print("Received event")

            if ev == DEFS.EF_ALARM:
                print("EF_ALARM:")
                alarm_code = z.parse_alarm_type()
                # check alarm source
                if alarm_code == 0x3A:
                    # misoperation
                    print("Misoperation alarm!")
                elif alarm_code == 0x37:
                    # tamper
                    print("Tampering alarm!")
                elif alarm_code == 0x35:
                    # exit button
                    print("Exit button pressed!")
                elif alarm_code == 0x54:
                    # door is closing
                    print("Door is closing")
                elif alarm_code == 0xffffffff:
                    # duress alarm
                    durr_type = z.parse_duress_alarm()[0]
                    if durr_type == 0x20:
                        print("Duress alarm!")
                        print("User index: %s, matching type: %i" %
                              tuple(z.parse_duress_alarm()[1:]))
                    elif durr_type == 0x22:
                        print("Passback alarm!")
                    else:
                        print("Unknown duress alarm")
                else:
                    print("Unknown alarm")

            elif ev == DEFS.EF_ATTLOG:
                print("EF_ATTLOG: New attendance entry")
                print("User id: %s, verify type %i, date: %s" %
                      tuple(z.parse_event_attlog()))

            elif ev == DEFS.EF_FINGER:
                print("EF_FINGER: Finger placed on reader")

            elif ev == DEFS.EF_ENROLLUSER:
                print("EF_ENROLLUSER: Enrolled user")

            elif ev == DEFS.EF_ENROLLFINGER:
                print("EF_ENROLLFINGER: Enroll finger finished")
                print("Successful: %s, user ID: %s, finger index: %s, "
                      "size fp template: %i" %
                      tuple(z.parse_event_enroll_fp()))

            elif ev == DEFS.EF_BUTTON:
                print("EF_BUTTON: Pressed button")

            elif ev == DEFS.EF_UNLOCK:
                print("EF_UNLOCK: Unlock event")

            elif ev == DEFS.EF_VERIFY:
                print("EF_VERIFY: Verified user")
                user_sn = z.parse_verify_event()
                if user_sn == 0xffffffff:
                    user_id = '-1'
                else:
                    user_id = z.users[user_sn].user_id
                print("User id: %s" % user_id)

            elif ev == DEFS.EF_FPFTR:
                print("EF_FPFTR: ")
                print("Score: %i" % z.parse_score_fp_event())

            else:
                print("Unknown event:")
                misc.print_hex(z.get_last_packet())

    except KeyboardInterrupt:
        misc.print_info("\nExiting...")

    z.disconnect()


if __name__ == "__main__":
    print("running manual test")
    opts = {'ip-address': "192.168.1.201"}
    test_realtime(opts)
