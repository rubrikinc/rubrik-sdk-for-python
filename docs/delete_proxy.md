# delete_proxy

Delete the proxy configuration from the Rubrik cluster.
```py
def delete_proxy(self, timeout=15)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The proxy configuration is already cleared out. |
| dict  | The full API response for `DELETE /internal/node_management/proxy_config`. |

## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

delete_proxy = rubrik.delete_proxy()
```
