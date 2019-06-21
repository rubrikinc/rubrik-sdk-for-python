# configure_replication_nat

Configure replication partner as specified by user using NAT gateways.
```py
def configure_replication_nat(username, password, source_gateway, target_gateway, ca_certificate, timeout)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username  | str  | The target Rubrik Cluster username used for authentication. |         |
| password  | str  | The target Rubrik Cluster password used for authentication. |         |
| source_gateway | list | Specification of source NAT gateway specified as `[str IP, [list of portnumber(s)]]`.  |         |
| target_gateway | list | Specification of target NAT gateway specified as `[str IP, [list of portnumber(s)]]`.  |         |

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| ca_certificate  | str  | CA certificiate used to perform TLS certificate validation  |         |    None     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| tuple  | The full API response for `POST /internal/replication/target"` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

remote_cluster_user = "testuser"
remote_cluster_password = "testpassword"
src_gateway = ["1.2.3.4",[1234]]
tgt_gateway = ["2.3.4.5",[1234]]

new_replication = rubrik.configure_replication_nat(remote_cluster_user, remote_cluster_password, src_gateway, tgt_gateway)
```
