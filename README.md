# PyZK #

Python lib to access ZKTeco's standalone devices

This project is part of an effort to make an alternative to the ZKTeco's software, to manage the attendance devices, it was made based on the protocol spec shown in [zk-protocol](https://github.com/adrobinoga/zk-protocol) repo.

## Tests ##

A series of tests scrips are included to test the library and to show
how the lib may be used, to perform common admin actions:

- Creating/modifying users.
- Creating groups.
- Enrolling users.
- Downloading/uploading fingerprint info.
- Monitor realtime events.

and more ...

## Documentation ##

The docs are generated with Sphinx, to generate the docs, `cd` to the docs dir and type

	$ make html

Then open the file index.html inside `docs/build/html` dir.

## Develop ##

Currently this lib is intended for devices of the TFT series, but there's no reason to keep it that way.

Make contributions to the develop branch under a pull request.

Capture files of network traffic of documented tests are welcomed, to expand the protocol spec and then add support in the lib.

## Contact ##

Author: Alexander Marin <alexanderm2230@gmail.com>