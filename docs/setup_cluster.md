# setup_cluster

Issues a bootstrap request to a specified Rubrik cluster
```py
def setup_cluster(self, cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, 
node_config=None, ipmi_config=None, ipmi_gateway=None, ipmi_subnet_mask=None, data_config=None, data_gateway=None,
data_subnet_mask=None, enable_encryption=True, dns_search_domains=None, dns_nameservers=None, ntp_servers=None,
wait_for_completion=True, timeout=30)
```

## Useage

### Physical Cluster or Virtual Appliance

By default, an un-bootstrapped Rubrik Cluster will respond to [multicast DNS](https://en.wikipedia.org/wiki/Multicast_DNS) (mDNS) queries directed to `[node_serial_number].local`. It is important that mDNS resolution is working properly on system the SDK is called from if you wish to supply `[node_serial_number].local` to the `bootstrap()` function as the `node_ip` value. 

| Note: When bootstrapping a cluster, `Bootstrap()` is used instead of `Connect()` to establish the connection to the cluster. |
| --- |


mDNS resolution is not well supported on Windows, but it can be accomplished by installing the Apple Bonjour service, included with [iTunes](https://www.apple.com/itunes/) or [Bonjour Print Services](https://support.apple.com/kb/DL999?locale=en_US). mDNS is better supported on Linux and macOS, but you should verify working name resolution before using this function. If mDNS name resolution is not working on Linux, you can determine the link-local IPv6 address of the un-bootstrapped node(s) with the command `avahi-resolve --name [node_serial_number].local` or by using the [python-zeroconf](https://pypi.org/project/zeroconf/) library. The link-local IPv6 address can then be passed to the `Bootstrap()` function instead of the mDNS name.

### Cloud cluster

Cloud Cluster instances have an IPv4 address dynamically assigned by the cloud provider, so there is no need to use mDNS for bootstrapping. Once the instances are deployed, gather the assigned IPs from the cloud provider console and use them in a similar manner to the example below.

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
| cluster_name  | str  | Unique name to assign to the Rubrik cluster. |         |
| admin_email  | str  | The Rubrik cluster sends messages for the admin account to this email address. |         |
| admin_password  | str  |  Password for the admin account. |         |
| management_gateway  | str  |  IP address assigned to the management network gateway |         |
| management_subnet_mask  | str  | Subnet mask assigned to the management network. |         |
| ipmi_gateway  | str  |  IP address assigned to the ipmi network gateway |         |
| ipmi_subnet_mask  | str  | Subnet mask assigned to the ipmi network. |         |
| data_gateway  | str  |  IP address assigned to the data network gateway |         |
| data_subnet_mask  | str  | Subnet mask assigned to the data network. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| node_config  | dict  | The Node IPs formatted as a dictionary.  |         |    None     |
| ipmi_config  | dict  | The Node IPMI IPs formatted as a dictionary.  |         |    None     |
| data_config  | dict  | The Node Data Network IPs formatted as a dictionary.  |         |    None     |
| enable_encryption  | bool  | Enable software data encryption at rest. When bootstraping a Cloud Cluster this value needs to be False.  |         |    True     |
| dns_search_domains  | str  | The search domain that the DNS Service will use to resolve hostnames that are not fully qualified.  |         |    None     |
| dns_nameservers  | list  | IPv4 addresses of DNS servers.  |         |    [8.8.8.8]     |
| ntp_servers  | list  | FQDN or IPv4 address of a network time protocol (NTP) server.  |         |    [pool.ntp.org]     |
| wait_for_completion  | bool  | Flag to determine if the function should wait for the bootstrap process to complete.  |         |    True     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response returned by `POST /internal/cluster/me/bootstrap`. |

## Examples

### Physical Cluster or Virtual Appliance

```py
import rubrik_cdm

node_ip = 'VRVW4217DB4E3.local'
# Alternatively:
# node_ip = 'fe80::250:56ff:fe97:31cf'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
node_config['RVMHMabcd002059'] = '192.168.0.10'
node_config['RVMHMabcd002088'] = '192.168.0.11'
node_config['RVMHMabcd000065'] = '192.168.0.12'
node_config['RVMHMabcd001185'] = '192.168.0.13'

ipmi_config = {}
ipmi_config['RVMHMabcd002059'] = '192.168.1.10'
ipmi_config['RVMHMabcd002088'] = '192.168.1.11'
ipmi_config['RVMHMabcd000065'] = '192.168.1.12'
ipmi_config['RVMHMabcd001185'] = '192.168.1.13'

data_config = None

cluster_name = 'Python-SDK'
admin_email = 'Drew.Russell@rubrik.com'
admin_password = 'A c0mpl3x p@ssw0rd!'

management_gateway = '192.168.0.1'
management_subnet_mask = '255.255.255.0'

ipmi_gateway = '192.168.1.1'
ipmi_subnet_mask = '255.255.255.0'

data_gateway = None
data_subnet_mask = None

enable_encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, management_gateway, 
                            management_subnet_mask, node_config, ipmi_config, ipmi_gateway, ipmi_subnet_mask, 
                            data_config, data_gateway, data_subnet_mask, enable_encryption, dns_search_domains,
                            dns_nameservers, ntp_servers, wait_for_completion)

print(setup_cluster)
```

### Cloud Cluster

```py
import rubrik_cdm

node_ip = '172.22.7.23'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
node_config['1'] = node_ip
node_config['2'] = '172.22.18.241'
node_config['3'] = '172.22.9.68'
node_config['4'] = '172.22.12.154'

ipmi_config = None
data_config = None

cluster_name = 'Python-SDK'
admin_email = 'Drew.Russell@rubrik.com'
admin_password = 'A c0mpl3x p@ssw0rd!'

management_gateway = '172.22.0.1'
management_subnet_mask = '255.255.240.0'

ipmi_gateway = None
ipmi_subnet_mask = None

data_gateway = None
data_subnet_mask = None

enable_encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, management_gateway, 
                            management_subnet_mask, node_config, ipmi_config, ipmi_gateway, ipmi_subnet_mask, 
                            data_config, data_gateway, data_subnet_mask, enable_encryption, dns_search_domains,
                            dns_nameservers, ntp_servers, wait_for_completion)

print(setup_cluster)
```
