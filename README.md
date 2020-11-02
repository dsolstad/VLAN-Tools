# vlancon.py

A tool to easily setup multiple VLAN interfaces on Linux. It will use the highest available IP-address unless you specify a IP-address in the last argument.  

Syntax:    
$ python3 vlancon.py add|rem &lt;network&gt; &lt;interface&gt; &lt;vlan&gt; [&lt;preferred ip-addr&gt;]

```
root@kali:~# python3 vlancon.py add 192.168.1.0/24 eth1 101
[+] Adding interface eth1.101 (192.168.1.0/24)  
[+] Interface added.
[+] Waiting for ARP table to update.
[+] Searching for other hosts in the VLAN.
[+] Found 24 live host in network 192.168.1.0/24
[+] Checking for an available IP-address.
[+] Using IP-address: 192.168.1.254/24
[+] Adding gateway.
[+] Gateway added.
root@kali:~#  
```
  
In order for vlancon.py to work, you need to have a connection to a trunk port of a switch. I recommend getting an Ethernet to USB dongle to have a seperate interface just for this.  
  
## Use cases and Tips

The following scenarios assumes that the gateways have the first available IP-address in each VLAN. For example: 192.168.1.1/24

### Routing traffic
If you want to route traffic through a certain VLAN, as for example Internet traffic, add a dafault route via the target VLANs gateway:
```
root@kali:~# python3 vlancon.py add 192.168.1.0/24 eth1 101
root@kali:~# ip route add default via 192.168.1.1
```

### Comma VLANs
If you encounter a VLAN with the name e.g. 101,2 you need to strip the comma part and use the subnet for the "parent" VLAN. Then manually add a static route to the target VLAN via a gateway. See the following example below:
  
VLAN List:
```
101    192.168.1.0/24
101,1  192.168.2.0/24
101,2  192.168.3.0/24
```

If you want a connection to 192.168.3.0/24, then do the following:
```
root@kali:~# python3 vlancon.py add 192.168.1.0/24 eth1 101
root@kali:~# ip route add 192.168.3.0/24 via 192.168.1.1
```

### Automate connection to multiple VLANs
If you want to connect to multiple VLANs simultaneously, then you could make a script like this:
```
root@kali:~# cat connect_all.sh
python3 vlancon.py add 192.168.1.0/24 eth1 101 &
python3 vlancon.py add 192.168.2.0/24 eth1 102 &
python3 vlancon.py add 192.168.3.0/24 eth1 103 &
python3 vlancon.py add 192.168.4.0/24 eth1 104 &
wait
exit
root@kali:~# ./connect_all.sh
```
  
