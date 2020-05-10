======
PyZatt
======


.. image:: https://img.shields.io/pypi/v/pyzatt.svg
        :target: https://pypi.python.org/pypi/pyzatt

.. image:: https://img.shields.io/travis/adrobinoga/pyzatt.svg
        :target: https://travis-ci.com/adrobinoga/pyzatt

.. image:: https://readthedocs.org/projects/pyzatt/badge/?version=latest
        :target: https://pyzatt.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/adrobinoga/pyzatt/shield.svg
     :target: https://pyup.io/repos/github/adrobinoga/pyzatt/
     :alt: Updates


**Python lib to access ZKTeco's standalone devices**

* Supports TFT and iFace(partial) devices, B&W devices are not supported yet.
* Documentation: https://pyzatt.readthedocs.io.
* Free software: MIT license

Introduction
------------

This project is part of an effort to make an alternative to ZKTeco's
software, to manage attendance devices, it was made using the protocol
spec shown in `zk-protocol <https://github.com/adrobinoga/zk-protocol>`_ repo.

Project overview
----------------

Functions in this module follow a similar grouping used on zk-protocol repo.

ZK Modules
**********
- **Access**: Includes functions to get/set access parameters (permissions,
  groups, timezones).
- **Data Record**: Includes functions to manage the attendance records and
  operation records.
- **Data User**: Includes functions to manage users info, including passwords,
  fingerprints, names, verification styles, etc).
- **Realtime**: Includes functions to receive and parse realtime events
  (e.g. user auth at door).
- **Terminal**: Includes functions to get/set device parameters.
- **Other**: Misc operations (enable/disable device, restart, power off, etc).

For more info about these operations
take a look at `zk-protocol <https://github.com/adrobinoga/zk-protocol>`_.

Tests
*****

A series of tests scrips are included to test the library and to show
how the lib may be used.
Some of the actions that can be done with these scripts include:

- Creating/modifying users.
- Creating groups.
- Enrolling users.
- Downloading/uploading fingerprint info.
- Monitor realtime events.

and more ...

For more details about running tests see docs/tests.rst

Check also docs/usage.rst to understand how to use the lib

Installation
------------

For more details see docs/installation.rst

Develop
-------

Currently this lib is intended for devices of the TFT series,
but there's no reason to keep it that way.

Capture files of network traffic of documented tests are welcomed,
to expand the protocol spec and then add support in the lib.

For more details see ./CONTRIBUTING.rst

Contact
-------

Author: Alexander Marin <alexuzmarin@gmail.com>
