#!/bin/python
##
## This is nothing else than a wrapper around nmap.
## Author: Daniel Solstad (dsolstad.com)
##

import sys
import os
import re
import subprocess
import time
import math
from termcolor import colored

help = """
vlanscan.py <target network> <src interface>

Example:
vlanman.py 192.168.1.0/24 eth1.101
"""

if not sys.version_info[0] == 3:
    print ("You need to run this with Python 3")
    sys.exit()

if len(sys.argv) != 3:
    print (colored('Missing one or more arguments', 'red'))
    print (help)
    sys.exit()

network = sys.argv[1]
interface = sys.argv[2]

top100_udp = "7,9,17,19,49,53,67-69,80,88,111,120,123,135-139,158,161-162,177,427,443,"
top100_udp += "445,497,500,514-515,518,520,593,623,626,631,996-999,1022-1023,1025-1030,"
top100_udp += "1433-1434,1645-1646,1701,1718-1719,1812-1813,1900,2000,2048-2049,2222-2223,"
top100_udp += "3283,3456,3703,4444,4500,5000,5060,5353,5632,9200,10000,17185,20031,30718,"
top100_udp += "31337,32768-32769,32771,32815,33281,49152-49154,49156,49181-49182,49185-49186,"
top100_udp += "49188,49190-49194,49200-49201,65024"

## Creating the output folder
results_dir = 'Results2/' + interface
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

#ipaddr, submask = target.split('/')

## Host discovery
## We need to do host discovery first to be able to get 
## the result from the port scan in different output files.

print ('[+] Initiating host discovery')
result = subprocess.check_output(['nmap', '-sn', network, '-e', interface])
# Extract all valid IP addresses
hosts = re.findall(b'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result)
# Convert the IP addresses to strings from byte-objects
hosts = [s.decode('ascii') for s in hosts] 

if len(hosts) > 0:
    print (colored('[+] Found the following hosts:', 'green'))
    print ("\n".join(hosts))
    print ('[+] Writing result to ' + results_dir + '/host_discovery.txt')
    with open(results_dir + '/host_discovery.txt' , 'w') as out:
        out.write("\n".join(hosts))
else:
    print (colored('[+] Found zero hosts. Aborting.', 'red'))
    sys.exit()

## Port scan

print ('----------------------------------------')

for host in hosts:
    print ('[+] Initiating port scan on ' + host)
    print ('[+] Storing result in ' + results_dir + '/' + host + '.*')

    cmd = ['nmap', '-sUT', host, '-T4', '-O', '-n', '-v', '-Pn',
           '-pT:1-65535,U:' + top100_udp,
           '--stats-every', '5s',
           '-e', interface,
           '-oA', results_dir + '/' + host]

    #Debug - Prints out the full nmap command
    #print (" ".join(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print ('[+] Connect scan progress')
    
    host_complete = False
    while host_complete is False:
        #time.sleep(0.5)
        for line in p.stdout:
            # Debug - Prints out output from nmap
            #print (line.rstrip())
            # Tracking connect scan progress
            match = re.search(b"Connect Scan Timing: About (.*?)%", line)
            if match:
                #print (match.group(1))
                curr = math.ceil(float(match.group(1).decode('ascii')) / 2) 
                print ('[' + (colored('X', 'yellow') * curr) + (" " * (50-curr)) + ']', end="\r")
            if line.find(b'Completed Connect Scan') != -1:
                print ('[' + (colored('X', 'yellow') * 50) +']', end="\r")
                print (colored('\n[+] Connect scan completed', 'green'))
                print ('[+] Service scan progress')

            # Tracking service scan progress
            match = re.search(b"Service scan Timing: About (.*?)%", line)
            if match:
                #print (match.group(1))
                curr = math.ceil(float(match.group(1).decode('ascii')) / 2) 
                print ('[' + (colored('X', 'yellow') * curr) + (" " * (50-curr)) + ']', end="\r")
                if line.find(b'Completed Service scan') != -1:
                    print ('[' + (colored('X', 'yellow') * 50) +']', end="\r")
                    print (colored('\n[+] Service scan completed', 'green'))
                    print ('[+] Finishing up...')

            # Checking if the scanning of the host is complete 
            match = re.search(b"Nmap done: 1 IP address", line)
            if match:
                print (colored('[+] Scanning of ' + host + ' completed', 'green'))
                host_complete = True
            else:
                sys.stdout.flush()
                break

