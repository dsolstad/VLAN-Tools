# VLAN-Tools

## vlanman.py - A tool to add and remove VLAN interfaces for Linux  
  
vlanman.py add <network> <netmask> <vlan nr> <interface> <gateway>  
vlanman.py rem <interface> <vlan nr> <gateway>  
  
Example:  
vlanman.py add 192.168.1.0 255.255.255.0 101 eth1 192.168.1.1  
vlanman.py rem eth1 101 192.168.1.1
