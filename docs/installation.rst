.. highlight:: shell

============
Installation
============

Setup
-----

In order to use PyZatt with your ZKTeco's attendance device you need to:

- Setup communication with your physical devices.
- Install PyZatt lib.

Then you can start building your own apps.

Physical Setup
--------------

Follow the Quick Start Guide,
found in here `<https://www.zkteco.me/product-details/f18>`_

Obviously, it is recommended to run tests on devices that are
not in use, because some tests can delete useful info on your device,
if you can't afford an exclusive device to perform testing before deploy
you can create a back up of your device(s) using ZKTeco's software.
That way you can restore users data in case something goes wrong.

To use your devices you need a working connection with them, in case
the device it is already on a VPN, just connect to this network.

In case you don't have that setup, you can simply connect your pc to your device
using a cross or straight network cable.
Then, setup a wired network on your PC with manual IPv4 addressing::

    IP Address: 192.168.1.124
    Subnet Mask:255.255.255.0

Write down the IP address of your device (given on Menu->System->Comm), you
will need this IP for running tests.

- Note that for newer ZKTeco's devices you can connect to the device using
  a straight or cross cable, so you don't need a switch or hub to start testing.
- Magnetic locks may include a kickback protection, so for some locks you may
  ignore setup with diode FR-107.

Stable release
--------------

To install PyZatt, run this command in your terminal::

    pip install pyzatt

This is the preferred method to install PyZatt, as it will always install
the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide:
  http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

You may use a virtualenv for installation.
I prefer handling virtual envs with virtualenvwrapper::

    sudo apt-get install virtualenvwrapper

Clone the project and create the virtual environment::

    git clone git://github.com/adrobinoga/pyzatt
    cd pyzatt
    mkvirtualenv -p $(which python3.6) -a . pyzatt

Then you can install the lib with::

    pip install .

For development tasks use::

    pip install -r requirements_dev.txt
    pip install -e .

This command will keep using the source files on the current folder,
that could be useful for dev & debugging.

Use::

    workon pyzatt

to start using the virtualenv and::

    deactivate

when you are finished
