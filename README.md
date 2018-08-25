# VLAN-Tools

## vlanman.py - A tool to add and remove VLAN interfaces on Linux  
  
vlanman.py add &lt;network&gt; &lt;netmask&gt; &lt;vlan nr&gt; &lt;interface&gt; &lt;gateway&gt;  
vlanman.py rem &lt;interface&gt; &lt;vlan nr&gt; &lt;gateway>  

**root@kali:~#** python3 vlanman.py add 192.168.1.0 255.255.255.0 101 eth0 192.168.1.1  
[+] Adding interface eth0.101 (192.168.1.0)  
[+] Interface added.  
[+] Checking for an available IP-address  
[+] Using IP-address: 253  
[+] Adding gateway 192.168.1.1  
[+] Gateway added.  
[+] Checking if gateway is responding  
