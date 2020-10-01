# update_proxy

Update the proxy configuration on the Rubrik cluster.

```py
def update_proxy(self, host, protocol, port, username=None, password=None, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| host  | str | The IP address or FQDN of the proxy you wish to add. |  |
| protocol  | str | The protocol of the proxy you wish to add. |  |
| port  | int | The port of the proxy you wish to add. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| username  | str | The username used for authentication.  |  | None |
| password  | str | The password used for authentication.  |  | None |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full API response for `PATCH /internal/node_management/proxy_config` |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

host = "proxy.python.demo"
protocol = "HTTPS"
port = 443

update_proxy = rubrik.update_proxy(host, protocol, port)
```
