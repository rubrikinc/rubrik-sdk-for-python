# configure_ntp

Configure connection information for the NTP servers used by the Rubrik cluster for time synchronization.

```py
def configure_ntp(self, ntp_server, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| ntp_server  | list | A list of the NTP server(s) you wish to configure the Rubrik cluster to use. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The NTP server(s) `ntp_server` has already been added to the Rubrik cluster. |
| dict | {'status_code': 204} |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ntp_servers = ["192.168.10.121", "192.168.10.122"]
configure_ntp = rubrik.configure_ntp(ntp_servers)

```
