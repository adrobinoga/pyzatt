#!/usr/bin/env python

import pytest
import time
import os.path
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as DEFS
import pyzatt.misc as misc

"""
Test script to test/show several functions of the access spec/lib.

The script test_other.py should be executed before this script, so the
fp templates fp1 and fp2 are available.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


@pytest.mark.skip()
def test_access(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    misc.print_header("TEST OF ACCESS FUNCTIONS")

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    misc.print_header("1.Read all user info")

    # delete test uses if they exists
    user1_id = "5555"
    user2_id = "6666"
    if z.id_exists(user1_id):
        z.delete_user(user1_id)
        z.delete_user(user2_id)

    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    misc.print_header("2.Create users and upload fingerprints")

    z.set_user_info(user_id=user1_id, name="Dummy 1",
                    password="22224444", card_no=333,
                    admin_lv=0, neg_enabled=0,
                    user_group=1, user_tzs=[1, 0, 0])

    z.set_user_info(user_id=user2_id, name="Dummy 2",
                    password="33335555", card_no=777,
                    admin_lv=0, neg_enabled=0,
                    user_group=1, user_tzs=[1, 0, 0])

    z.read_all_user_id()
    z.set_verify_style(user1_id, DEFS.GROUP_VERIFY)
    z.set_verify_style(user2_id, DEFS.GROUP_VERIFY)

    fp1_tmp = bytearray()
    fp1_fn = 'fp1.bin'  # filename template 1
    fp1_idx = 8  # finger index template 1
    fp1_flg = 1  # finger flag template 1

    fp2_tmp = bytearray()
    fp2_fn = 'fp2.bin'  # filename template 2
    fp2_idx = 7  # finger index template 2
    fp2_flg = 1  # finger flag template 2, duress

    # read previously generated templates
    if os.path.isfile(fp1_fn) and os.path.isfile(fp2_fn):
        with open(fp1_fn, 'rb') as infile:
            fp1_tmp = infile.read()
        with open(fp2_fn, 'rb') as infile:
            fp2_tmp = infile.read()

        misc.print_info("Uploading templates")
        print("Upload template 1, user= %s, finger=%i, flag=%i" %
              (user1_id, fp1_idx, fp1_flg))
        z.upload_fp(user1_id, fp1_tmp, fp1_idx, fp1_flg)

        print("Upload template 2, user= %s, finger=%i, flag=%i" %
              (user1_id, fp2_idx, fp2_flg))
        z.upload_fp(user2_id, fp2_tmp, fp2_idx, fp2_flg)

        misc.print_info("Now the templates should be available")
        z.read_all_user_id()
        z.read_all_fptmp()
        z.print_users_summary()

    else:
        print("Run the script test_data_other.py before this script!")
        z.enable_device()
        z.disconnect()

    misc.print_header("3. Set/get timezones")

    print("Timezone 1:", z.get_tz_info(1))
    z.set_tz_info(49, z.get_tz_info(1))

    tz49 = z.get_tz_info(49)
    print("Timezone 49:", tz49)

    sat_tz = [5, 33, 23, 20]
    print("Changing Sat tz:", sat_tz)
    tz49[6] = sat_tz
    z.set_tz_info(49, tz49)  # uploading update timezone

    print("New timezone 49:", z.get_tz_info(49))

    misc.print_header("4. Creating groups")

    z.set_group_info([35, [1, 49], 0, 1])
    z.set_group_info([36, [1, 49], 0, 1])

    print("Group 35: %s" % z.get_group_info(35))
    print("Group 36: %s" % z.get_group_info(36))

    print("Adding user %s to group 35" % user1_id)
    print("Adding user %s to group 36" % user2_id)

    z.set_user_group(user1_id, 35)
    z.set_user_group(user2_id, 36)

    print("New group of user %s: %i" % (user1_id, z.get_user_group(user1_id)))
    print("New group of user %s: %i" % (user2_id, z.get_user_group(user2_id)))

    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    misc.print_header("5. Users timezones")

    for n in range(3):
        tz_no = 40 + n
        print("Creating timezone: ", tz_no)
        z.set_tz_info(tz_no, z.get_tz_info(1))

    print("Setting user %s timezones" % user1_id)
    user1_tzs = [40, 41, 42]
    z.set_user_tzs(user1_id, user1_tzs)
    print("User %s should be using timezones: %s" % (user1_id, user1_tzs))

    print("Making user %s, use group's timezones" % user2_id)
    z.disable_user_tzs(user2_id)

    z.read_all_user_id()
    z.print_users_summary()

    misc.print_header("6. Unlock combinations")

    misc.print_info("Creating unlock combination")

    z.set_unlock_comb(9, [35, 36])
    print("Created unlock combination %i, with groups: %s" %
          (9, z.get_unlock_comb(9)))

    misc.print_header("7. Unlock door")

    print("Door unlock: 20 seconds")
    time.sleep(10)
    z.door_unlock(20)

    misc.print_header("")

    misc.print_info("Now to test this configuration, press [n], go to the"
                    "device and you should need both fingers (corresponding "
                    "to the templates) to get access, because both belong to "
                    "different users and from different groups, and they are "
                    "in an unlock combination.")

    ans = input("Delete users %s, y/n: " % user1_id)
    if ans == 'y':
        z.delete_user(user1_id)
        z.delete_user(user2_id)
    else:
        misc.print_info("Now you may go and test access with "
                        "both finger templates")

    misc.print_header("")
    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    z.enable_device()
    z.disconnect()
