# configure_ntp

Configure the Rubrik cluster timezone.
```py
def configure_ntp(ntp_server)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| ntp_server  | list  | A list of the NTP server(s) you wish to configure the Rubrik cluster to use. |         |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The NTP server(s) `ntp_server` has already been added to the Rubrik cluster. |
| dict  | {'status_code': 204} |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ntp_servers = ["192.168.10.121", "192.168.10.122"]
configure_ntp = rubrik.cluster_ntp(ntp_servers)
```