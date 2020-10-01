# configure\_vlan

Configure VLANs on the Rubrik cluster.

```python
def configure_vlan(self, vlan, netmask, ips, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| vlan | int | The VLAN ID you wish to configure. |  |
| netmask | str | The netmask of the VLAN ID you wish to configure. |  |
| ips | list or dict | The `ips` argument can either be a list or a dictionary. The list should contain an IP, in the relevant VLAN, for each node in the cluster. These IPs will be sorted, from lowest to highest, and then automatically associated with a node name based on alphabetical order. If you would like more finite control over the assignment you can use a dict with `node_name:ip` as it's key pairs. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The Rubrik cluster is already configured with the provided VLAN information. |
| dict | The full API response for `POST /internal/cluster/me/vlan'` |

## Example

```python
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
```

