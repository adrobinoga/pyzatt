=============
Running Tests
=============

Introduction
------------

Tests may be executed with tox, or pytest, I show both ways so you may chose
which you find more useful for your particular needs.

Before you begin
****************
Obviously, it is recommended to run tests on devices that are
not in use, because some tests can delete useful info on your device,
if you can't afford an exclusive device to perform testing before deploy
you can create a back up of your device(s) using ZKTeco's software.
That way you can restore users data in case something goes wrong.

Using Pytest
------------

First, install the dev requirements::

    pip install -r dev_requirements.txt

and the pyzatt lib::

    pip install -e .

Now, you should be able to see the custom options for tests::

    pytest --help

Currently there are three options:

- platform
- ip-address
- seed (wip)

Now to run a test you may use the name of the file, but that will run all the
test given on a file, or you may use a keyword.

To run test_terminal test you may use::

    pytest --ip-address=192.168.1.201 test_terminal.py

or::

    pytest --ip-address=192.168.1.201 -k test_terminal

If you want to see what is printed by the test, use -s option::

    pytest --ip-address=192.168.1.201 -s -k test_terminal

To check which tests are about to run with an specific command you can use
the --collect-only option::

        pytest --ip-address=192.168.1.201 -s -k realtime --collect-only

This shows 2 tests::

    <Module test_multiple_realtime.py>
        <Function test_multiple_realtime>
    <Module test_realtime.py>
        <Function test_realtime>

You can also use markers, tests are marked just before their the declaration.
To match manual tests use ``manual`` tag::

    pytest --ip-address=192.168.1.201 -m manual --collect-only

Additional notes
****************

- Platform options is by default ``hardware``, the second option is to
  use ``simulator``, but this is hasn't been implemented yet,
  same as ``seed`` option.
- When you are using pytest you will be using the python and pyzatt
  version you have installed, so if you created a py36 env then
  it will be executed using py36.
- If you try to run manual tests you'll find they are skipped, to get the test
  able to execute the skip mark needs to be removed manually, in the future
  the idea is to use another param to force skipped tests execution.

Using Tox
---------

If you already have installed dev requirements, then you are ready to go.
The cool thing about tox is that it takes care of package and lib install
for test running, and you can even chose which python version to use,
so you don have to bother with creation of virtualenvs::

    tox -e (env) -- (pytest options)

Where the ``env`` may be:

- py36
- py37
- py38
- flake8 (code checks)

and the ``pytest options`` are the same given above.
So the command to run the terminal test with python3.8 would be::

    tox -e py38 -- --ip-address=192.168.1.201 -s -k test_terminal
