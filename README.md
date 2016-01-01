# PyFi
A Python 3 based wifi monitor that utilizes [nmap](https://nmap.org) and AT&T's [M2X](https://m2x.att.com) to track devices connected to a local network. 


## What you need
* Familiarity with the AT&T [M2X API](https://m2x.att.com/developer/documentation/v2/overview).
* Raspberry Pi running [RaspBian](http://www.raspbian.org) or another unix system capable of running nmap v6.01+.
* A free AT&T [M2X Account](https://m2x.att.com/signup).

## Dependencies

* Python3 running on your chosen machine
* [nmap](https://nmap.org) installed on your machine - written for v6.01+
* [m2x-python](https://github.com/attm2x/m2x-python) - written for v4.0.0+
* [python-nmap](https://pypi.python.org/pypi/python-nmap) - written for v0.3.4
* [netifaces](https://pypi.python.org/pypi/netifaces) - written for v0.10.4


## Instructions

1. Clone this repository
2. In keys.txt replace `<MASTER_API_KEY>`
with your master api key. [Here's a direct link](https://m2x.att.com/account#master-keys).

3. Run master.py on your machine

    ```bash
    $ sudo python3 master.py
    ```

4. Log in to M2X, access your device, and you will see data about your local wifi network!


## Troubleshooting

Make sure the version of nmap installed is at least v6.01 or else reading MAC addresses will not be possible.

If you are running Raspbian on a Raspberry Pi, the easiest way to go about it is to run Raspbian Jessie instead of Raspbian Wheezy. This way the packages installed with `apt-get` are all up to date.

A common issue installing netifaces with pip is that you are missing header files for python. If this happens try installing python3-dev on your machine (`sudo apt-get install python3-dev`).

## License

This library is released under the MIT license. See ``LICENSE`` for the terms.

