# setup_cluster

Issues a bootstrap request to a specified Rubrik cluster
```py
def setup_cluster(self, cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, node_mgmt_ips,
                  mgmt_vlan=None, ipmi_gateway=None, ipmi_subnet_mask=None, ipmi_vlan=None, node_ipmi_ips=None,
                  data_gateway=None, data_subnet_mask=None, data_vlan=None,
                  node_data_ips=None, enable_encryption=True, dns_search_domains=None, dns_nameservers=None,
                  ntp_servers=None, wait_for_completion=True, timeout=30):
```

## Usage

When bootstrapping nodes the `Bootstrap()` function is used to establish the connection. It allows the user to specify an interface name, which is the local network interface that will be used to connect to the Rubrik node(s). If you are attempting a bootstrap from a system with multiple interfaces, you should set this parameter. If no interface is specified, the SDK will attempt to use the first non-loopback interface it finds. Below is the specification for the Bootstrap() function.

```py
def Bootstrap(node_ip, interface=None, enable_logging=False)
```
### Physical Cluster

Bootstrapping a physical cluster will only be possible using IPv6 (see mDNS below). Management and IPMI configurations are mandatory for a successful bootstrap.

### Virtual Appliance

When bootstrapping a Virtual Appliance (Edge), this can be done either by using the IPv4 address as set on deployment or using IPv6 as stated below. IPMI addresses and DATA addresses can not be set and the encryption parameter should be set to "False".

### Cloud cluster

Cloud Cluster instances have an IPv4 address dynamically assigned by the cloud provider, so there is no need to use mDNS for bootstrapping. Once the instances are deployed, gather the assigned IPs from the cloud provider console and use them in a similar manner to the example below. Cloud Clusters need to have the encryption parameter set to "False".

### mDNS

By default, an un-bootstrapped Rubrik node will respond to [multicast DNS](https://en.wikipedia.org/wiki/Multicast_DNS) (mDNS) queries directed to `[node_serial_number].local`. It is important that mDNS resolution is working properly on system where the SDK is called from if you wish to supply `[node_serial_number].local` to the `Bootstrap()` function as the `node_ip` value. 

Any un-bootstrapped nodes on a network can be found using "avahi-browse -a" (Linux) or using a packet tracing utility filtering on mDNS (port 5353 - any OS).

mDNS resolution is not well supported on Windows, but it can be accomplished by installing the Apple Bonjour service, included with [iTunes](https://www.apple.com/itunes/) or [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US). mDNS is better supported on Linux and macOS, but you should verify working name resolution before using this function. If mDNS name resolution is not working on Linux, you can determine the link-local IPv6 address of the un-bootstrapped node(s) with the command `avahi-resolve --name [node_serial_number].local` or by using the [python-zeroconf](https://pypi.org/project/zeroconf/) library. The link-local IPv6 address can then be passed to the `Bootstrap()` function instead of the mDNS name.

## Troubleshooting

Enable logging by passing `enable_logging=True` to the bootstrap function. Example:

```
bootstrap = rubrik_cdm.Bootstrap(node_ip, enable_logging=True)
```

mDNS name resolution can be verified on systemd-based Linux systems using the command `systemd-resolve --status`. The resulting command should display `MulticastDNS setting: resolve` or `MulticastDNS setting: yes`. Additional information can be found at the links below.

* https://wiki.archlinux.org/index.php/Systemd-resolved
* https://wiki.archlinux.org/index.php/Systemd-networkd

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| cluster_name | str | Unique name to assign to the Rubrik cluster. No FQDN allowed with dots. |         |
| admin_email | str | The Rubrik cluster sends messages for the admin account to this email address. |         |
| admin_password | str | Password for the admin account. Store carefully. |         |
| mgmt_gateway | str | IP address assigned to the management network gateway. |         |
| mgmt_subnet_mask | str | Subnet mask assigned to the management network. |         |
| node_mgmt_ips | dict | The Node Name(s) and IP(s) formatted as a dictionary for Management addresses. |         |

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| mgmt_vlan | int | VLAN assigned to the management network. | | None |
| ipmi_gateway  | str |  IP address assigned to the ipmi network gateway. | | None |
| ipmi_subnet_mask  | str | Subnet mask assigned to the ipmi network. | | None |
| ipmi_vlan  | int | VLAN assigned to the ipmi network. | | None |
| node_ipmi_ips  | dict | The Node Name and IP formatted as a dictionary for IPMI addresses. Optional. | | None |
| data_gateway  | str |  IP address assigned to the ipmi network gateway. | | None |
| data_subnet_mask  | str | Subnet mask assigned to the ipmi network. | | None |
| data_vlan  | int | VLAN assigned to the data network. | | None |
| node_data_ips  | dict | The Node Name and IP formatted as a dictionary for Data addresses. Optional. | | None |
| enable_encryption  | bool | Enable software data encryption at rest. For Cloud Cluster or Edge this value needs to be False. | | True |
| dns_search_domains  | str | The search domain that the DNS Service will use to resolve hostnames that are not fully qualified. | | None |
| dns_nameservers  | list | IPv4 addresses of DNS servers. | | ['8.8.8.8'] |
| ntp_servers  | list | FQDN or IPv4 address of a network time protocol (NTP) server. | | ['pool.ntp.org'] |
| wait_for_completion  | bool | Flag to determine if the function should wait for the bootstrap process to complete. | | True |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | | 30 | 

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response returned by `POST /internal/cluster/me/bootstrap`. |

## Examples

### Physical Cluster Example

```py
import rubrik_cdm

## IPv6 only. mDNS broadcast - avahi daemon
node_ip = 'SERIAL1.local'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

## Alternatively, specify local interface
## interface = 'ens160'
## bootstrap = rubrik_cdm.Bootstrap(node_ip, interface)

node_config = {}
ipmi_config = {}
data_config = {}

node_config['SERIAL1'] = '10.10.10.10'
node_config['SERIAL2'] = '10.10.10.12'
node_config['SERIAL3'] = '10.10.10.13'
node_config['SERIAL4'] = '10.10.10.14'

ipmi_config['SERIAL1'] = '10.10.10.15'
ipmi_config['SERIAL2'] = '10.10.10.16'
ipmi_config['SERIAL3'] = '10.10.10.17'
ipmi_config['SERIAL4'] = '10.10.10.18'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'
ipmi_gateway = '10.10.10.1'
ipmi_subnet_mask = '255.255.255.0'
data_gateway = None
data_subnet_mask = None
dns = ['10.10.10.2']
encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway,mgmt_subnet_mask,node_config, None,
                                        ipmi_gateway, ipmi_subnet_mask,None,ipmi_config,
                                        data_gateway,data_subnet_mask,data_vlan,None,
                                        encryption, None, dns)
print(setup_cluster)
```
### Virtual Appliance Example

```py
import rubrik_cdm

## Examples of specifying IPs (v4 or v6 possible)
## node_ip = '10.10.10.10'
## node_ip = 'fe80::250:250:250:250'
node_ip = 'SERIAL.local'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}

node_config['SERIAL.local'] = '10.10.10.10'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.10.1'
mgmt_subnet_mask = '255.255.255.0'

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, 
										node_config, enable_encryption=False)

print(setup_cluster)
```

### Cloud Cluster Example

```py
import rubrik_cdm

## IPv4 only bootstrap.
node_ip = '10.10.10.10'

bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}

node_config['SERIAL1'] = '10.10.10.10'
node_config['SERIAL2'] = '10.10.10.11'
node_config['SERIAL3'] = '10.10.10.12'
node_config['SERIAL4'] = '10.10.10.13'

cluster_name = 'CLUSTERNAME'
admin_email = 'admin@company.com'
admin_password = 'SafePassword!'
mgmt_gateway = '10.10.60.1'
mgmt_subnet_mask = '255.255.255.0'

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, mgmt_gateway, mgmt_subnet_mask, 
										node_config, enable_encryption=False)

print(setup_cluster)
```
