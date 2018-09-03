# VLAN-Tools

## vlanloopscan.py - A tool to scan multiple vlans automatically

$ vlanloopscan.py &lt;path/to/vlanlist.txt&gt; [&lt;path/to/ports.txt&gt]

## vlancon.py - A tool to add and remove VLAN interfaces on Linux  
  
$ vlancon.py add &lt;network&gt;/24 &lt;interface&gt; &lt;vlan&gt; &lt;gateway&gt;  
$ vlancon.py rem &lt;interface&gt; &lt;vlan nr&gt; &lt;gateway&gt;  

```
root@kali:~# python3 vlancon.py add 192.168.1.0/24 eth0 101 192.168.1.1  
[+] Adding interface eth0.101 (192.168.1.0)  
[+] Interface added.  
[+] Checking for an available IP-address   
[+] Successfully set IP-address: 192.168.1.254  
[+] Adding gateway 192.168.1.1  
[+] Gateway added.  
[+] Checking if gateway is responding  
[+] Success. Gateway responding.  
root@kali:~#  
```
  
## nmapscan.py - A wrapper around nmap  

$ nmapscan.py &lt;network&gt; &lt;interface&gt;
```
root@kali:~# python3 nmapscan.py 192.168.1.0/24 eth0.101  
[+] Initiating host discovery  
[+] Found the following hosts:  
192.168.1.1  
192.168.1.2  
192.168.1.137  
192.168.1.254  
[+] Writing result to Results/192.168.1.0[24]/host_discovery.txt  
----------------------------------------  
[+] Initiating port scan on 192.168.1.1  
[+] Storing result in Results/eth0.101/192.168.1.1.*  
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
