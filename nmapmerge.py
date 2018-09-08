#!/usr/bin/env python3
##
## A tool to merge multiple nmap scans into CSV
## Author: Daniel Solstad (dsolstad.com)
##

import sys

if not sys.version_info[0] == 3:
    print ("You need to run this with python3")
    sys.exit()

import os
import re
from termcolor import colored

help = """
nmapmerge.py <path/to/folder>

The script expects .nmap files directly inside the input folder.
"""

if len(sys.argv) != 2:
    print (help)
    sys.exit(1)

folder = sys.argv[1]
results = []

print ('[+] Merging files in the folder: ' + folder)

for filename in os.listdir(folder):

    # Skip files not ending with .nmap
    if not filename.endswith('.nmap'):
        continue

    path = os.path.join(folder, filename)
    print ('[+] Opening: ' + path)

    with open(path) as f:

        for line in f.readlines():
            match = re.match('(\d+)\/(tcp|udp)\s+(.*?)\s+(.*?)\s+(.*?)', line)
            if match:
                try:
                    info = {'ipaddr': os.path.splitext(filename)[0],
                            'port': match.group(1),
                            'protocol': match.group(2),
                            'state': match.group(3),
                            'service': match.group(4),
                            'version': match.group(5)}
                    results.append(dict(info))
                except: pass


with open('services.csv', 'w') as f:
    # Print CSV headers
    for item in results[0].keys():
        f.write(item + ',')
    # Print CSV values
    for x in results:
        f.write("\n")
        for key, value in x.items():
            f.write(value + ',')

print (colored('[+] Written merged CSV result to ' + os.getcwd() + '/services.csv', 'green'))
