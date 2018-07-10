#!/usr/bin/python3.5

import time
import datetime
from utils import *
import pyzk.pyzk as pyzk
import pyzk.zkmodules.defs as defs
from pyzk.misc import *

"""
Test script to test/show parsing functions of the realtime spec/lib.

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

print_header("TEST OF REALTIME FUNCTIONS")

# connection
print_header("1.Realtime Test")
z.connect_net(ip_address, machine_port)

print_info("Ready to receive events from the machine")

try:
    while True:
        # wait for event
        z.recv_event()
        ev = z.get_last_event()

        # process the event
        print("Received event")

        if ev == EF_ALARM:
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

        elif ev == EF_ATTLOG:
            print("EF_ATTLOG: New attendance entry")
            print("User id: %s, verify type %i, date: %s" %
                  z.parse_event_attlog())

        elif ev == EF_FINGER:
            print("EF_FINGER: Finger placed on reader")

        elif ev == EF_ENROLLUSER:
            print("EF_ENROLLUSER: Enrolled user")

        elif ev == EF_ENROLLFINGER:
            print("EF_ENROLLFINGER: Enroll finger finished")
            print("Successful: %s, user ID: %s, finger index: %s, "
                  "size fp template: %i" %
                  tuple(z.parse_event_enroll_fp()))

        elif ev == EF_BUTTON:
            print("EF_BUTTON: Pressed button")

        elif ev == EF_UNLOCK:
            print("EF_UNLOCK: Unlock event")

        elif ev == EF_VERIFY:
            print("EF_VERIFY: Verified user")
            print("User id: %s" % tuple(z.parse_verify_event()))

        elif ev == EF_FPFTR:
            print("EF_FPFTR: ")
            print("Score: %i" % z.parse_score_fp_event())

        else:
            print("Unknown event:")
            print_h(z.get_last_packet())

except KeyboardInterrupt:
    print_info("\nExiting...")

z.disconnect()
exit(0)
