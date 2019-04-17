# setup_cluster

Issues a bootstrap request to a specified Rubrik cluster
```py
def setup_cluster(cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, node_config=None,
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| cluster_name  | str  | Unique name to assign to the Rubrik cluster. |         |
| admin_email  | str  | The Rubrik cluster sends messages for the admin account to this email address. |         |
| admin_password  | str  |  Password for the admin account. |         |
| management_gateway  | str  |  IP address assigned to the management network gateway |         |
| management_subnet_mask  | str  | Subnet mask assigned to the management network. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| node_config  | dict  | The Node Name and IP formatted as a dictionary.  |         |    None     |
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
## Example
```py
import rubrik_cdm

node_ip = '172.22.13.66'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

node_config = {}
node_config['1'] = node_ip
node_config['2'] = '172.22.18.241'
node_config['3'] = '172.22.9.68'
node_config['4'] = '172.22.12.154'

cluster_name = 'Python-SDK'
admin_email = 'Drew.Russell@rubrik.com'
admin_password = 'RubrikGoForward'
management_gateway = '172.22.0.1'
management_subnet_mask = '255.255.240.0'

enable_encryption = False

setup_cluster = bootstrap.setup_cluster(cluster_name, admin_email, admin_password, management_gateway,
                                        management_subnet_mask, node_config, enable_encryption)

print(setup_cluster)
```