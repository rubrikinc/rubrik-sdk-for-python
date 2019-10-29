# status

Searches for nodes bootstrappable to the specified Rubrik cluster
```py
def discover(timeout=30)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The response timeout value, in seconds, of the API call.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response returned by `GET /internal/cluster/me/discover`. |

## Example
```py
import rubrik_cdm

node_ip = '172.22.13.66'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

discovered_nodes = bootstrap.discover()

print(discovered_nodes)
```
