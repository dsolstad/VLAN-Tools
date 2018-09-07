#!/usr/bin/env python3
##
## A tool to easily add and remove vlans
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
vlancon.py add|rem <network/<cidr>> <interface> <vlan nr>

Example:
vlancon.py add 192.168.1.0/24 eth1 101
vlancon.py rem 192.168.1.0/24 eth1 101
"""

def vlan_add(interface, vlan):
    subinterface = interface + "." + vlan
    sub.call(['vconfig', 'add', interface, vlan], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ip', 'link', 'set', 'dev', interface, 'up'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ip', 'link', 'set', 'dev', subinterface, 'up'], stdout=sub.PIPE, stderr=sub.PIPE)

def vlan_rem(interface, vlan):
    subinterface = interface + "." + vlan
    sub.call(['ip', 'link', 'set', 'dev', interface, 'down'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ip', 'link', 'set', 'dev', subinterface, 'down'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['vconfig', 'rem', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)

def set_ip_addr(interface, vlan, ipaddr):
    subinterface = interface + "." + vlan
    sub.call(['ip', 'addr', 'add', ipaddr, 'dev', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)

def gateway_add(network, interface, vlan):
    subinterface = interface + "." + vlan    
    #sub.call(['ip', 'route', 'add', 'default', 'via', gateway, 'dev', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ip', 'route', 'add', network, 'dev', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)

def gateway_rem(network, interface, vlan):
    subinterface = interface + "." + vlan    
    #sub.call(['ip', 'route', 'del', 'default', 'via', gateway, 'dev', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ip', 'route', 'del', network, 'dev', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)

# Checks for an available IP-address. Trying to get the highest available.
def get_ip_addr(interface, vlan, network):
    cmd = ['arp-scan', '--interface=' + interface + '.' + vlan , network, '--arpspa', '0.0.0.0']
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    res, err = p.communicate()
    # Filter out all valid IP addresses
    ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', res.decode('ascii'))
    # Loop through and return the highest available IP address
    # Debug: print(get_ip_range(network, netmask))
    cidr = network.split('/')
    for addr in reversed(get_ip_range(network)):
        if addr not in ips:
            return addr + '/' + cidr[1]
    return False

# Waiting for the network to be ready. 
# If the ARP table gets populated before 100 seconds, 
#  we can jump right to the arp scan.
def wait_for_arp(interface, vlan, network):
    subinterface = interface + '.' + vlan
    for i in range(1, 100):
        try:
            res = sub.check_output(['arp', '-a', '-i', subinterface]).decode('ascii')
            # If there no incomplete entries we return
            if res.find('incomplete') == -1 and res.find('no match') == -1:
                return True
        except: pass
        time.sleep(1)
    return False

# Checking if the gateway is responsive. Waiting 60 seconds.
def check_gateway(gateway):
    for i in range(1, 60):
        try:
            res = sub.check_output(['ping', '-c', '1', gateway]).decode('ascii')
            if res.find('1 received') != -1:
                return True
        except:
            time.sleep(1)
    return False

# Gets the last octet of all valid IP addresses in the network range
def get_ip_range(network):
    net = ipaddress.ip_network(network)
    ip_range = []
    for addr in list(map(str, net.hosts())):
        ip_range.append(addr)
    return ip_range


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print (help)
        sys.exit(1)

    if sys.argv[1] == 'rem':
        if len(sys.argv) != 5:
            print (colored('Missing one or more arguments', 'red'))
            print (help)
            sys.exit(1)

        interface = sys.argv[2]
        vlan = sys.argv[3]
        #gateway = sys.argv[4]

        print ('[+] Removing vlan interface: ' + interface + '.' + vlan)
        vlan_rem(interface, vlan)
        print ('[+] Removing gateway: ' + gateway)
        gateway_rem(interface, vlan, gateway)
        print (colored('Done.', 'green'))

    elif sys.argv[1] == 'add':
        if len(sys.argv) != 5:
            print (colored('Missing one or more arguments', 'red'))
            print (help)
            sys.exit(1)

        network = sys.argv[2]       # e.g 192.168.1.0/24
        interface = sys.argv[3]     # e.g eth1
        vlan = sys.argv[4]          # e.g 101
        #gateway = sys.argv[5]       # e.g 192.168.1.1
        
        #print ("[+] ")
        print ('[+] Adding interface ' + interface + '.' + vlan + ' (' + network + ')')
        vlan_rem(interface, vlan)
        vlan_add(interface, vlan)
        print (colored('[+] Interface added.', 'green'))
        
        print ('[+] Waiting for ARP table to update.')
        wait_for_arp(interface, vlan, network)

        print ('[+] Checking for an available IP-address')
        ipaddr = get_ip_addr(interface, vlan, network)
        if ipaddr != False:
            set_ip_addr(interface, vlan, ipaddr)
            print (colored('[+] Using IP-address: ' + str(ipaddr), 'green'))
        else:
            print (colored('[+] Error - Could not find any available IP addresses. Aborting.', 'red'))
            sys.exit(1)
        
        print ("[+] Adding gateway ")
        gateway_add(network, interface, vlan)
        print (colored('[+] Gateway added.', 'green'))

        #print ("[+] Checking if gateway is responding")
        #if check_gateway(gateway):
        #print (colored('[+] Success. Gateway responding.', 'green'))
        #else:
        #    print (colored('[+] Error - No respons from gateway.', 'red'))
        #    sys.exit(1)

    else:
        print (colored('Missing one or more arguments', 'red'))
        print (help)
        sys.exit(1)

