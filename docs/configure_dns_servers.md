# configure_dns_servers

Configure the DNS Servers on the Rubrik cluster.
```py
def configure_dns_servers(server_ip, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| server_ip  | list  | The DNS Server IPs you wish to add to the Rubrik cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster is already configured with the provided DNS servers. |
| dict  | The full API response for `POST /internal/cluster/me/dns_nameserver'` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

dns_server_ip = ["192.168.100.21", "192.168.100.22"]
cluster_dns_servers = rubrik.cluster_dns_servers(dns_server_ip)
```