# PyFi
A Python 3 based network monitor that utilizes [nmap](https://nmap.org) to report devices connected to a local network and sends that information to AT&T's [M2X](https://m2x.att.com).

See https://pyfi.herokuapp.com to see PyFi data being displayed by the [PyFi-Web demo](https://github.com/sterlzbd/pyfi-monitor-web) flask application.

## What you need
* Familiarity with the AT&T [M2X API](https://m2x.att.com/developer/documentation/v2/overview).
* Raspberry Pi running [RaspBian](http://www.raspbian.org) or another unix system capable of running nmap v6.01+.
* A free AT&T [M2X Account](https://m2x.att.com/signup).

## Dependencies

* Python3 running on your chosen machine
* [nmap](https://nmap.org) installed on your machine - written for v6.01+
* [m2x-python](https://github.com/attm2x/m2x-python) - written for v4.0.0+
* [python-nmap](https://pypi.python.org/pypi/python-nmap) - written for v0.3.4+
* [netifaces](https://pypi.python.org/pypi/netifaces) - written for v0.10.4


## Instructions

1. Clone this repository
2. In keys.txt replace `<MASTER_API_KEY>`
with your master api key. [Here's a direct link](https://m2x.att.com/account).
3. Install dependencies:
    ```bash
    $ sudo apt-get install nmap
    ```

    ```bash
    $ pip3 install -r requirements.txt
    ```

4. Run master.py on your machine

    ```bash
    $ sudo python3 master.py
    ```

5. Log in to M2X, access your device, and you will see data about your local wifi network!

** If something does go wrong, check errors.log in the directory containing master.py (/home/pi/pyfi-monitor-m2x/)

## Optional: Run as a service using systemd

First, check if your system is using systemd. You'll know by running `man init` and seeing which program's man page you end up on.

The unit file included in this repo (pyfi.service) can be used by systemd to run PyFi as a service that start on system start-up and will auto restart in the event of an unforseen crash. Follow the instructions given in the file to customize it for your setup.

Then follow these steps:

1. Copy pyfi.service to default location used by systemd.

    ```bash
    $ cp /home/pi/pyfi-monitor-m2x/pyfi.service /lib/systemd/system/pyfi.service
    ```
2. Set correct permissions on the unit file.

    ```bash
    $ chmod 644 /lib/systemd/system/pyfi.service
    ```
3. Load the service into systemd.

    ```bash
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable pyfi.service
    ```
4. Now PyFi will automatically start when your machine boots or manually start it using `sudo systemctl start pyfi`.
You can check on it's status with `sudo systemctl status pyfi` and stop it with `sudo systemctl stop pyfi`.


## Troubleshooting

Make sure the version of nmap installed is at least v6.01 or else reading MAC addresses will not be possible.

If you are running Raspbian on a Raspberry Pi, the easiest way to go about it is to run Raspbian Jessie instead of Raspbian Wheezy. This way the packages installed with `apt-get` are all up to date.

A common issue installing netifaces with pip is that you are missing header files for python. If this happens try installing python3-dev on your machine (`sudo apt-get install python3-dev`).

## License

This library is released under the MIT license. See ``LICENSE`` for the terms.

