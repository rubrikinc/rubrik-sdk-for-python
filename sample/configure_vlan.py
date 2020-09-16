import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vlan = 100
netmask = "255.255.255.0"

# List of an IP for each node in the cluster
ips = ["192.168.1.100", "192.168.1.101", "192.168.1.102",
       "192.168.1.103", "192.168.1.104", "192.168.1.105", "192.168.1.106", "192.168.1.107"]

vlan = rubrik.configure_vlan(vlan, netmask, ips)

# Dict with node_name:ip as it's key pairs.
ips = {'RVM015S011553': '192.168.1.100', 'RVM015S011884': '192.168.1.101', 'RVM015S011922': '192.168.1.102',
       'RVM016S006406': '192.168.1.103',
       'RVM01AS007435': '192.168.1.104', 'RVM01AS012299': '192.168.1.105', 'RVM01AS025280': '192.168.1.106',
       'RVM01AS025323': '192.168.1.107'}

vlan = rubrik.configure_vlan(vlan, netmask, ips)
