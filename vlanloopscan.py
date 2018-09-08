#!/usr/bin/env python3
##
## This tools nmap scans every vlan in the input list
## Author: Daniel Solstad (dsolstad.com)
##

import sys

if not sys.version_info[0] == 3:
    print ("You need to run this with python3")
    sys.exit()

import os
import time
import re
import subprocess as sub
import ipaddress
from termcolor import colored

help = """
vlanloopscan.py <path/to/vlanlist.txt> [<path/to/ports.txt>]

vlanlist.txt:
<network/<cidr>> <interface> <vlan nr>

vlanlist.txt example:
192.168.1.0/24,eth0,101
192.168.2.0/24,eth0,102

The optional ports file needs to contain TCP ports on line 1 and UDP ports on line 2 (comma separated).
If no ports file present it will scan all 1 to 65535 tcp and top 100 udp ports

ports.txt:
<comma separated tcp ports>
<comma separated udp ports>

ports.txt example:
80,443,445,8080
67,68,69
"""

filename_vlan = sys.argv[1]

with open(filename_vlan) as lines:
    for line in lines:
        args = line.split(',')
        network, interface, vlan = args[0], args[1], args[2]
        
        # Add the vlan interface
        sub.call(['python3 ./vlancon.py', 'add', network, interface, vlan])

        if len(sys.argv) == 2:
            filename_ports = sys.argv[2]
            cmd = ['python3', './nmapscan.py', network, interface, filename_ports]
        else:
            cmd = ['python3', './nmapscan.py', network, interface]

        p = sub.call(cmd)

        # Remove the vlan interface
        sub.call(['python3 ./vlancon.py', 'rem', network, interface, vlan])
