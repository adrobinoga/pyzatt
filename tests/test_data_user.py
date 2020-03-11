#!/usr/bin/env python

import os.path
import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as DEFS

"""
Test script to test/show several functions of the data-user spec/lib.

The script test_other.py should be executed before this script, so the
fp templates fp1 and fp2 are available.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that will
    overwrite any changes made by the script.

Author: Alexander Marin <alexuzmarin@gmail.com>
"""


def test_data_user(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    misc.print_header("TEST OF DATA-USER FUNCTIONS")

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)
    z.disable_device()

    misc.print_header("1.Read all user info")

    # delete user if it exists
    user1_id = "5555"
    if z.id_exists(user1_id):
        z.delete_user(user1_id)

    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    misc.print_header("2.Changing verification mode")

    # set user params
    z.set_user_info(user_id=user1_id, name="Dummy 1",
                    password="22224444", card_no=333,
                    admin_lv=0, neg_enabled=0,
                    user_group=1, user_tzs=[1, 0, 0])
    z.read_all_user_id()
    z.set_verify_style(user1_id, DEFS.GROUP_VERIFY)

    print("User: %s" % user1_id)
    print("Verify style: %i" % z.get_verify_style(user1_id))
    z.set_verify_style(user1_id, DEFS.FPorRF)
    print("New verify style: %i" % z.get_verify_style(user1_id))

    misc.print_header("3. Clear and set password")

    print("Users password: %s" % z.get_password(user1_id))
    z.clear_password(user1_id)
    z.set_password(user1_id, "99")
    print("New password is: %s" % z.get_password(user1_id))

    misc.print_header("4. Uploading/deleteting templates")

    fp1_tmp = bytearray()
    fp1_fn = 'fp1.bin'  # filename template 1
    fp1_idx = 8  # finger index template 1
    fp1_flg = 1  # finger flag template 1

    fp2_tmp = bytearray()
    fp2_fn = 'fp2.bin'  # filename template 2
    fp2_idx = 7  # finger index template 2
    fp2_flg = 3  # finger flag template 2, duress

    # delete the templates if they already exists
    z.delete_fp(user1_id, fp1_idx)
    z.delete_fp(user1_id, fp2_idx)

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
        z.upload_fp(user1_id, fp2_tmp, fp2_idx, fp2_flg)

        misc.print_info("Now the templates should be available")
        z.read_all_user_id()
        z.read_all_fptmp()
        z.print_users_summary()

    else:
        print("Run the script test_data_other.py before this script!")
        z.enable_device()
        z.disconnect()
    return

    ans = input("Delete user %s, y/n: " % user1_id)
    if ans == 'y':
        z.delete_user(user1_id)
    else:
        misc.print_info("Now you may go and test both finger templates")

    misc.print_header("")
    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    z.enable_device()
    z.disconnect()
