# configure_syslog

Configure the Rubrik cluster syslog settings..
```py
def configure_syslog(syslog_ip, protocol, port=514, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| syslog_ip  | str  | The IP address or hostname of the syslog server you wish to add to the Rubrik cluster. |         |
| protocol  | str  | The protocol to use when making the connection to the syslog server.  |    TCP, UDP     |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| port  | int  | The port to use when making the connection to the syslog server.  |         |    514     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster is already configured to use the syslog server '`syslog_hostname`' on port '`port`' using the '`protocol`' protocol. |
| dict  | The full API response for `POST /internal/syslog'` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

syslog_ip = "192.168.1.208"
protocol = "UDP"

syslog = rubrik.cluster_syslog(syslog_ip, protocol)
```