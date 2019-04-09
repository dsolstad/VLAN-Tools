# VLAN-Tools

A collection of scripts that can be useful when doing network assessments with nmap in multiple VLANs.  
  
## vlancon.py - Add and remove VLAN interfaces on Linux  
  
$ vlancon.py add|rem &lt;network&gt; &lt;interface&gt; &lt;vlan&gt; [&lt;preferred ip-addr&gt;]

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
  
If you encounter a VLAN with the name e.g. 101,2 you need to strip the comma part and use the subnet for the "parent" VLAN. Then manually add a static route to the target VLAN via a gateway. See the following example below. Assuming 192.168.1.1 is a gateway.
  
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
  
If you want to connect to multiple VLANs simultaneously, then you could make a script like this:
```
root@kali:~# cat connect_all.sh
./vlancon.py add 192.168.1.0/24 eth1 101 &
./vlancon.py add 192.168.2.0/24 eth1 102 &
./vlancon.py add 192.168.3.0/24 eth1 103 &
./vlancon.py add 192.168.4.0/24 eth1 104 &
root@kali:~# ./connect_all.sh
```
  
## segtest.py - Optimized Nmap scan for segmentation testing

When doing a blind network scan, where every host is reported to be alive and all ports filtered, a large network scan will take forever to complete. After benchmarking Nmap and comparing results with different settings, including max-rtt-timeout,host-timeout,max-retries and min/max-hostgroup it was the rtt-timeout parameter that did the most decrease in scan time. A value of 150ms resulted in the fastest and most thorough scan for the network I assessed. Any lower value would fail to find all active services. 
  
$ python3 segtest.py &lt;network&gt;
  
Tip: You can use xargs to do multiple Nmap scans in parallel. Just be sure to find the right number for your network, before you start to lose accuracy. The targets.txt can contain any number of subnets (separated by newlines). The following command will only run three Nmap processes simultaneously at any given time until the all the targets are scanned.
  
```
$ cat targets.txt | xargs -I CMD -P 3 python3 segtest.py
```

