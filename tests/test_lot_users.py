#!/usr/bin/env python

import pytest
import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt

"""
Test script to test/show several functions of the data-user spec/lib.

Reads a list of users from users.csv and then it deletes them one by one.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


@pytest.mark.skip()
def test_lot_users(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    misc.print_header("TEST OF DATA-USER FUNCTIONS")

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    misc.print_header("1.Read all user info")
    z.read_all_user_id()
    z.print_users_summary()

    misc.print_header("2.Creating users")

    users_fn = 'users.csv'  # filename of the user list
    n = 0  # counter, used for card number field
    added_users_ids = []  # keeps track of added users

    misc.print_info("Reading users from %s file" % users_fn)
    with open(users_fn, 'r') as infile:
        infile.readline()  # skip headers
        for line in infile.read().splitlines():
            # extract fields from a line
            user_fields = line.split(',')
            user_id = user_fields[0]
            user_name = "%s %s" % tuple(user_fields[1:3])
            user_tzs = [int(user_fields[3]), 0, 0]
            user_password = user_fields[4]

            # grow list of users, they will be deleted
            # WARNING, existing users with the same ID will be deleted
            added_users_ids += [user_id]

            if z.id_exists(user_id):
                print("OOOPS, user exists with the given id, "
                      "ID = %s, name = % s" %
                      (user_id, z.users[z.id_to_sn(user_id)].user_name))
            else:
                print("User ID = %s, name = % s" % (user_id, user_name))

                # add user with the given fields
                z.set_user_info(user_id=user_id, name=user_name,
                                password=user_password, card_no=n,
                                admin_lv=0, neg_enabled=0,
                                user_group=1, user_tzs=user_tzs)
                n += 1

    misc.print_info("After creating users")
    z.read_all_user_id()
    z.print_users_summary()

    misc.print_header("3.Deleting users")
    for uid in added_users_ids:
        print("Deleting user, ID = %s, name = % s" %
              (uid, z.users[z.id_to_sn(uid)].user_name))
        z.delete_user(uid)

    misc.print_info("After deleting users")
    z.read_all_user_id()
    z.print_users_summary()

    z.enable_device()
    z.disconnect()
    exit(0)
