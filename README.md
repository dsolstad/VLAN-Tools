# VLAN-Tools

## vlanloopscan.py - A tool to nmap scan multiple VLANs automatically

$ vlanloopscan.py &lt;path/to/vlanlist.txt&gt; [&lt;path/to/ports.txt&gt;]

## vlancon.py - A tool to add and remove VLAN interfaces on Linux  
  
$ vlancon.py add|rem &lt;network&gt; &lt;interface&gt; &lt;vlan&gt;  

```
root@kali:~# python3 vlancon.py add 192.168.1.0/24 eth0 101  
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

$ nmapscan.py &lt;network&gt; &lt;interface&gt; [&lt;path/to/ports.txt&gt;]
```
root@kali:~# python3 nmapscan.py 192.168.1.0/24 eth0.101
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

## nmapmerge.py - Merge multiple nmap ouputs into one CSV
$ nmapmerge.py &lt;path/to/folder&gt;
```
root@kali:~/Desktop# python3 nmapmerge.py Results/192.168.253.0[24]
[+] Merging files in the folder: Results/192.168.253.0[24]
[+] Opening: Results/192.168.253.0[24]/192.168.253.254.nmap
[+] Opening: Results/192.168.253.0[24]/192.168.253.2.nmap
[+] Written merged CSV result to /root/Desktop/services.csv
root@kali:~/Desktop# cat services.csv 
ipaddr,port,protocol,state,service,version,
192.168.253.254,80,tcp,filtered,http,,
192.168.253.254,443,tcp,filtered,https,,
192.168.253.254,445,tcp,filtered,microsoft-ds,,
192.168.253.254,8080,tcp,filtered,http-proxy,,
192.168.253.254,137,udp,open|filtered,netbios-ns,,
192.168.253.254,138,udp,open|filtered,netbios-dgm,,
192.168.253.254,139,udp,open|filtered,netbios-ssn,,
192.168.253.2,80,tcp,open,http,,
192.168.253.2,443,tcp,closed,https,,
192.168.253.2,445,tcp,closed,microsoft-ds,,
192.168.253.2,8080,tcp,closed,http-proxy,,
192.168.253.2,137,udp,open|filtered,netbios-ns,,
192.168.253.2,138,udp,open|filtered,netbios-dgm,,
192.168.253.2,139,udp,open|filtered,netbios-ssn,,
root@kali:~/Desktop# 
```
