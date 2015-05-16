# PyFi
A Python 3 based wifi monitor that utilizes [nmap](https://nmap.org) and AT&T's [M2X](https://m2x.att.com) to track devices connected to a local network. 


## What you need
* Familiarity with the AT&T [M2X API](https://m2x.att.com/developer/documentation/v2/overview).
* Raspberry Pi running [RaspBian](http://www.raspbian.org) or another unix system capable of running nmap.
* A free AT&T [M2X Account](https://m2x.att.com/signup).

## Dependencies

* Python3 running on your chosen machine
* [nmap](https://nmap.org) installed on your machine
* [m2x-python](https://github.com/attm2x/m2x-python) - written for v4.0.0
* [python-nmap](https://pypi.python.org/pypi/python-nmap) - written for v0.3.4


## Instructions

1. Clone this repository
2. In keys.txt replace `<MASTER_API_KEY>`
with your master api key. [Here's a direct link](https://m2x.att.com/account#master-keys).

3. Run master.py on your machine

    ```bash
    $ sudo python3 master.py
    ```

4. Log in to M2X, access your device, and you will see data about your local wifi network!


## License

This library is released under the MIT license. See ``LICENSE`` for the terms.

