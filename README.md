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
  
## nmapscan.py - Nmap scanning simplified  
This is just a wrapper around Nmap which will run a full host discovery, tcp, udp, os and version scan. It will also create output files for each host in all formats.
  
$ nmapscan.py &lt;network&gt; &lt;interface&gt; [&lt;path/to/ports.txt&gt;]
```
root@kali:~# python3 nmapscan.py 192.168.1.0/24 eth1.101
[+] No input file with ports given. Using defaults.
[+] Initiating host discovery  
[+] Found the following hosts:  
192.168.1.1  
192.168.1.2  
192.168.1.137  
192.168.1.254  
[+] Writing result to Results/192.168.1.0[24]/host_discovery.txt  
----------------------------------------  
[+] Initiating port scan on 192.168.1.1  
[+] Writing result to Results/192.168.1.0[24]/192.168.1.1/  
[+] Connect scan progress  
[XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]  
[+] Connect scan completed  
[+] Service scan progress  
[XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]  
[+] Scanning of 192.168.253.1 completed  
[+] Initiating port scan on 192.168.1.2
...  
root@kali:~#
```

The output folder structure example:
```
Results/192.168.0.0[24]  
       /192.168.1.0[24]/host_discovery.txt  
                        192.168.1.1/  
                        192.168.1.2/  
                        192.168.1.137/  
                        192.168.1.254/192.168.1.254.nmap  
                                      192.168.1.254.xml  
                                      192.168.1.254.gnmap  
  
```

## nmapmerge.py - Merge multiple Nmap ouputs into one CSV
$ nmapmerge.py &lt;path/to/folder&gt;
```
root@kali:~# python3 nmapmerge.py Results/
ipaddr,port,protocol,state,service,version,
192.168.1.254,80,tcp,filtered,http,,
192.168.1.254,443,tcp,filtered,https,,
192.168.1.254,445,tcp,filtered,microsoft-ds,,
192.168.1.254,8080,tcp,filtered,http-proxy,,
192.168.1.254,137,udp,open|filtered,netbios-ns,,
192.168.1.254,138,udp,open|filtered,netbios-dgm,,
192.168.1.254,139,udp,open|filtered,netbios-ssn,,
192.168.1.2,80,tcp,open,http,,
192.168.1.2,443,tcp,closed,https,,
192.168.1.2,445,tcp,closed,microsoft-ds,,
192.168.1.2,8080,tcp,closed,http-proxy,,
192.168.1.2,137,udp,open|filtered,netbios-ns,,
192.168.1.2,138,udp,open|filtered,netbios-dgm,,
192.168.1.2,139,udp,open|filtered,netbios-ssn,,
root@kali:~# 
```

## nmapunique.py - Get unique ports from Nmap scans
$ nmapunique.py &lt;path/to/folder&gt;
```
root@kali:~# python3 nmapunique.py Results/
21,22,23,25,53,80,81,88,89,111,135,139,161,389,427,443,445
root@kali:~# 
```

## segtest.py - Optimized Nmap scan for segmentation testing

When doing a blind network scan, where every host is reported to be alive and all ports filtered, a large network scan will take forever to complete. After benchmarking Nmap and comparing results with different settings, including max-rtt-timeout,host-timeout,max-retries and min/max-hostgroup it was the rtt-timeout parameter that did the most decrease in scan time. A value of 150ms resulted in the fastest and most thorough scan for the network I assessed. Any lower value would fail to find all active services. 
  
$ python3 segtest.py &lt;network&gt;
  
Tip: You can use xargs to do multiple Nmap scans in parallel. Just be sure to find the right number for your network, before you start to lose accuracy. The targets.txt can contain any number of subnets (separated by newlines), but only three Nmap processes will run simultaneously at any given time.
  
```
$ cat targets.txt | xargs -I CMD -P 3 python3 segtest.py
```

## vlanloopscan.py - Nmap scan multiple VLANs automatically

$ vlanloopscan.py &lt;path/to/vlanlist.txt&gt; [&lt;path/to/ports.txt&gt;]
  
