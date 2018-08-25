# VLAN-Tools

## vlanman.py - A tool to add and remove VLAN interfaces on Linux  
  
vlanman.py add &lt;network&gt; &lt;netmask&gt; &lt;vlan nr&gt; &lt;interface&gt; &lt;gateway&gt;  
vlanman.py rem &lt;interface&gt; &lt;vlan nr&gt; &lt;gateway>  
  
Example:  
vlanman.py add 192.168.1.0 255.255.255.0 101 eth1 192.168.1.1  
vlanman.py rem eth1 101 192.168.1.1
