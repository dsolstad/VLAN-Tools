#!/bin/python3
##
## This is nothing else than a wrapper around nmap.
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

def vlan_add(network, netmask, vlan, interface):
    subinterface = interface + "." + vlan
    sub.call(['ifconfig', interface, 'down'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ifconfig', subinterface, 'down'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['vconfig', 'rem', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['vconfig', 'add', interface, vlan], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['ifconfig', interface, 'up'], stdout=sub.PIPE, stderr=sub.PIPE)
    
def vlan_rem(interface, vlan):
    subinterface = interface + "." + vlan
    sub.call(['ifconfig', subinterface, 'down'], stdout=sub.PIPE, stderr=sub.PIPE)
    sub.call(['vconfig', 'rem', subinterface], stdout=sub.PIPE, stderr=sub.PIPE)

def set_ip_addr(interface, vlan, ip_addr, netmask):
    subinterface = interface + "." + vlan
    sub.call(['ifconfig', subinterface, ip_addr, 'netmask', netmask, 'up'], stdout=sub.PIPE, stderr=sub.PIPE)

def gateway_add(gateway):
    sub.check_output(['route', 'add', 'default', 'gw', gateway])

def gateway_rem(gateway):
    sub.check_output(['route', 'del', 'default', 'gw', gateway])

# Checks for an available IP-address. Trying to get the highest available.
def get_ip_addr(interface, vlan, network, netmask):
    subinterface = interface + "." + vlan
    cmd = ['arp-scan', '--interface=' + subinterface, network + '/' + str(mask2bits(netmask))]
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    res, err = p.communicate()
    # Filter out all valid IP addresses
    ips = re.findall(b"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", res)
    # Loop through and return the highest available IP address
    # Debug: print(get_ip_range(network, netmask))
    for addr in reversed(get_ip_range(network, netmask)):
        if addr not in ips:
            return addr
    return False

# Checking if the gateway is responsive. Waiting 60 seconds.
def check_gateway(gateway):
    for i in range(1, 60):
        try:
            res = sub.check_output(['ping', '-c', '1', gateway])
            if res.find('1 received') != -1:
                return True
        except:
            time.sleep(1)
    return False

# Gets the last octet of all valid IP addresses in the network range
def get_ip_range(network, netmask):
    net = ipaddress.ip_network(network + "/" + netmask)
    ip_range = []
    for addr in list(map(str, net.hosts())):
        ip_range.append(addr)
    return ip_range

# Converts netmask to CIDR. 255.255.255.0 -> /24
def mask2bits(netmask):
    return sum([bin(int(x)).count("1") for x in netmask.split(".")])


if __name__ == "__main__":

    help = """
    vlancon.py add <network> <netmask> <vlan nr> <interface> <gateway>
    vlancon.py rem <interface> <vlan nr> <gateway>

    Example:
    vlancon.py add 192.168.1.0 255.255.255.0 101 eth1 192.168.1.1
    vlancon.py rem eth1 101 192.168.1.1
    """    

    if len(sys.argv) == 1:
        print (help)
        sys.exit()

    if sys.argv[1] == 'rem':
        if len(sys.argv) != 4:
            print (colored('Missing one or more arguments', 'red'))
            print (help)
            sys.exit()

        interface = sys.argv[2]
        vlan = sys.argv[3]
        gateway = sys.argv[4]

        print ('[+] Removing vlan interface: ' + interface + '.' + vlan)
        vlan_rem(interface, vlan)
        print ('[+] Removing gateway: ' + gateway)
        gateway_rem(gateway)
        print (colored('Done.', 'green'))

    elif sys.argv[1] == 'add':
        if len(sys.argv) != 7:
            print (colored('Missing one or more arguments', 'red'))
            print (help)
            sys.exit()

        network = sys.argv[2]
        netmask = sys.argv[3]
        vlan = sys.argv[4]
        interface = sys.argv[5]
        gateway = sys.argv[6]
        
        #print ("[+] ")
        print ('[+] Adding interface ' + interface + '.' + vlan + ' (' + network + ')')
        vlan_add(network, netmask, vlan, interface)
        print (colored('[+] Interface added.', 'green'))
        print ('[+] Checking for an available IP-address')
        ip_addr = get_ip_addr(interface, vlan, network, netmask)
        if ip_addr != False:
            set_ip_addr(interface, vlan, ip_addr, netmask)
            print (colored('[+] Successfully set IP-address: ' + str(ip_addr), 'green'))
        else:
            print (colored('[+] Error - Could not find any available IP addresses. Aborting.', 'red'))
            sys.exit()
        
        print ("[+] Adding gateway " + gateway)
        gateway_add(gateway)
        print (colored('[+] Gateway added.', 'green'))
        print ("[+] Checking if gateway is responding")
        if check_gateway(gateway):
            print (colored('[+] Success. Gateway responding.', 'green'))
        else:
            print (colored('[+] Error - No respons from gateway.', 'red'))
            sys.exit()

    else:
        print (colored('Missing one or more arguments', 'red'))
        print (help)
        sys.exit()
