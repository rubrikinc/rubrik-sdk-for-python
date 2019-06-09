# cluster_support_tunnel

Enable or Disable the support tunnel.
```py
def cluster_support_tunnel(enabled=True, timeout=15)
```

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| enabled  | bool | The flag that enables or disables the support tunnel.  |    True, False     |    True   |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns

| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  |  No change required. Support Tunnel is already enabled.|
| str  |  No change required. Support Tunnel is already disabled.|
| dict  | The full API response from `POST /internal/node/me/support_tunnel. |


## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

enable_support_tunnel = rubrik.cluster_support_tunnel(True)
```



```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

disabled_support_tunnel = rubrik.cluster_support_tunnel(False)
```