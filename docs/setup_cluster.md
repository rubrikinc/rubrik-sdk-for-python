# setup_cluster

Issues a bootstrap request to a specified Rubrik cluster
```py
def setup_cluster(cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, node_config=None, enable_encryption=True, dns_search_domains=None, dns_nameservers=None, ntp_servers=None, wait_for_completion=True, timeout=30)
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
import rubrik

# Bootsgrap a Cluster
```